# airobloxbuilder training

this directory contains the training pipeline for the builder's specialized ai agents.

## agents

- orchestrator
- code
- gameplay
- world
- assets
- animation
- audio
- ui
- npc
- networking
- testing
- repair
- optimization
- documentation

each agent has its own dataset and output namespace. the pipeline can train one agent or all agents.

training is intentionally separate from the desktop application. model weights and large datasets are never bundled into the normal .exe or .app.

## commands

```
python training/train.py --agent code --model <base-model> --dataset training/datasets/code.jsonl
python training/train.py --all --model <base-model>
python training/validate.py
```

the trainer uses the optional transformers/torch stack when installed. dataset validation and manifest generation work without those heavy dependencies.

do not automatically train on private user projects. training data must be explicitly supplied, permitted, synthetic, or otherwise licensed for training.
