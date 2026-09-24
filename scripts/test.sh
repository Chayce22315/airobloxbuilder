#!/usr/bin/env bash
set -euo pipefail
cargo test --manifest-path src/core/Cargo.toml
python3 -m compileall ai
cmake -S src/native -B build/native
cmake --build build/native