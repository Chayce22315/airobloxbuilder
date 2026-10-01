import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "datasets"
REGISTRY = ROOT / "model_registry.json"


def load_rows(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict) or not row.get("prompt") or not row.get("response"):
                raise ValueError(f"{path}:{line_number}: expected prompt and response")
            yield row


def validate_dataset(path: Path) -> int:
    count = sum(1 for _ in load_rows(path))
    if count == 0:
        raise ValueError(f"{path}: dataset is empty")
    return count


def load_config(agent: str) -> dict:
    config = json.loads(REGISTRY.read_text(encoding="utf-8"))
    try:
        return config["models"][agent]
    except KeyError as exc:
        raise ValueError(f"no model configuration exists for agent {agent!r}") from exc


def train_qlora(agent: str, model_name: str, dataset: Path, output: Path, epochs: float, config: dict):
    validate_dataset(dataset)

    try:
        import torch
        from datasets import Dataset
        from peft import LoraConfig
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            BitsAndBytesConfig,
        )
        from trl import SFTConfig, SFTTrainer
    except ImportError as exc:
        raise RuntimeError(
            "QLoRA dependencies are optional; install torch, transformers, datasets, "
            "accelerate, peft, bitsandbytes, and trl"
        ) from exc

    if not torch.cuda.is_available():
        raise RuntimeError(
            "QLoRA training requires a CUDA-capable GPU. Use the GitHub factory's "
            "self-hosted GPU runner instead of a normal GitHub-hosted runner."
        )

    rows = list(load_rows(dataset))
    records = [
        {
            "prompt": row["prompt"],
            "completion": row["response"],
        }
        for row in rows
    ]
    data = Dataset.from_list(records)

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    quantization = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=quantization,
        # Keep the quantized model entirely on the RTX 5060. This avoids the
        # bitsandbytes CPU/disk dispatch failure seen with larger checkpoints.
        device_map={"": 0},
        trust_remote_code=True,
    )

    model.config.use_cache = False

    lora = LoraConfig(
        r=int(config.get("lora_r", 16)),
        lora_alpha=int(config.get("lora_alpha", 32)),
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules="all-linear",
    )

    training_args = SFTConfig(
        output_dir=str(output),
        num_train_epochs=epochs,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=int(config.get("gradient_accumulation_steps", 32)),
        learning_rate=float(config.get("learning_rate", 1e-4)),
        logging_steps=5,
        save_strategy="epoch",
        report_to=[],
        max_length=int(config.get("max_seq_length", 4096)),
        completion_only_loss=True,
        fp16=True,
        gradient_checkpointing=True,
        packing=True,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=data,
        processing_class=tokenizer,
        peft_config=lora,
    )
    trainer.train()
    trainer.save_model(output)
    tokenizer.save_pretrained(output)

    metadata = {
        "agent": agent,
        "base_model": model_name,
        "method": "qlora",
        "examples": len(rows),
        "epochs": epochs,
        "config": config,
    }
    (output / "training_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"fine-tuned {agent}: {len(rows)} examples -> {output}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True)
    parser.add_argument("--model")
    parser.add_argument("--dataset")
    parser.add_argument("--method", choices=["qlora"], default="qlora")
    parser.add_argument("--epochs", type=float, default=1.0)
    parser.add_argument("--output", default="training/artifacts")
    args = parser.parse_args()

    config = load_config(args.agent)
    model_name = args.model or config["model_id"]
    dataset = Path(args.dataset) if args.dataset else DEFAULT_DATA / f"{args.agent}.jsonl"
    output = Path(args.output) / args.agent
    output.mkdir(parents=True, exist_ok=True)

    train_qlora(
        args.agent,
        model_name,
        dataset,
        output,
        args.epochs,
        config,
    )


if __name__ == "__main__":
    main()
