# airobloxbuilder specialist model factory

the factory fine-tunes existing open-weight local models into airobloxbuilder specialists.

## current base checkpoints

- **code:** `Qwen/Qwen3.5-9B`
- **design:** `google/gemma-4-E4B-it`
- **animation:** `Qwen/Qwen3.5-4B`
- **testing:** `Qwen/Qwen3.5-4B`

these are base checkpoints. they are not airobloxbuilder-trained models yet.

the selections are intentionally small enough to be practical compared with current frontier coding models. the 9B code model is the heavier specialist; the other three keep the factory more manageable.

## training method

the factory uses **qlora**, not full-model training.

that means:

1. download the selected base model
2. load it in 4-bit
3. freeze the base weights
4. train a small lora adapter
5. save the adapter and tokenizer
6. benchmark the adapter
7. only promote it if it passes the specialist evaluation suite

the base model is never overwritten.

## github actions

the normal GitHub-hosted runner only validates datasets.

actual fine-tuning uses a self-hosted runner with labels:

`self-hosted, linux, x64, gpu`

the runner needs a working NVIDIA/CUDA stack.

run:

`actions -> airo specialist fine-tuning factory -> run workflow`

then choose:

- `code`
- `design`
- `animation`
- `testing`

an optional model override is available for experiments.

## hardware note

the user's current 8 GB GPU should be treated as a constrained QLoRA target. the factory therefore keeps sequence length, batch size and gradient accumulation conservative.

larger specialist checkpoints can be trained on a stronger self-hosted GPU without changing the dataset format.

## data rule

do not automatically train on private user projects.

training examples must be explicitly supplied, permitted, synthetic, or otherwise licensed for training.
