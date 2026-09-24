import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "datasets"

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

def train(agent: str, model_name: str, dataset: Path, output: Path):
    count = validate_dataset(dataset)
    try:
        from datasets import Dataset
        from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
    except ImportError as exc:
        raise RuntimeError(
            "training dependencies are optional; install torch, transformers, datasets, and accelerate to train models"
        ) from exc

    rows = list(load_rows(dataset))
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    def tokenize(row):
        text = f"### instruction\n{row['prompt']}\n### response\n{row['response']}"
        return tokenizer(text, truncation=True, max_length=2048)

    data = Dataset.from_list(rows).map(tokenize)
    args = TrainingArguments(
        output_dir=str(output),
        num_train_epochs=1,
        per_device_train_batch_size=1,
        save_strategy="epoch",
        logging_steps=10,
        report_to=[],
    )
    Trainer(model=model, args=args, train_dataset=data).train()
    model.save_pretrained(output)
    tokenizer.save_pretrained(output)
    print(f"trained {agent}: {count} examples -> {output}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent")
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--output", default="training/artifacts")
    args = parser.parse_args()

    manifest = json.loads((ROOT / "agents.json").read_text(encoding="utf-8"))
    agents = manifest["agents"] if args.all else [args.agent]
    if not agents or agents == [None]:
        parser.error("--agent or --all is required")

    for agent in agents:
        dataset = Path(args.dataset) if args.dataset and not args.all else DEFAULT_DATA / f"{agent}.jsonl"
        train(agent, args.model, dataset, Path(args.output) / agent)

if __name__ == "__main__":
    main()
