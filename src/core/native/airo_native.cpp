#include "airo_native.hpp"

#include <cstddef>

std::uint64_t airo_hash_bytes(const std::uint8_t* data, std::size_t length) {
    std::uint64_t hash = 14695981039346656037ull;
    for (std::size_t i = 0; i < length; ++i) {
        hash ^= data[i];
        hash *= 1099511628211ull;
    }
    return hash;
}

std::uint32_t airo_protocol_version() {
    return 1;
}
