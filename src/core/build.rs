fn main() {
    cc::Build::new()
        .cpp(true)
        .file("native/airo_native.cpp")
        .flag_if_supported("-std=c++17")
        .compile("airo_native");
}
