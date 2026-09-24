#pragma once
#include <cstddef>
#include <cstdint>

extern "C" {
std::uint64_t airo_hash_bytes(const std::uint8_t* data, std::size_t length);
std::uint32_t airo_protocol_version();
}
