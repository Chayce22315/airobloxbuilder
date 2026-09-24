#pragma once
#include <cstdint>
#include <string>
namespace airo { struct health_result { std::int32_t version; const char* status; }; health_result health(); std::string normalize_request(const std::string& text); }