$ErrorActionPreference = "Stop"
cargo test --manifest-path src/core/Cargo.toml
cmake -S native/cpp -B native/cpp/build
cmake --build native/cpp/build --config Release
