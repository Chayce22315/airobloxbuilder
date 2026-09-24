#pragma once
#include <string>
#include <vector>
namespace airo::native { struct Health { bool ok; std::string message; }; Health health(); std::vector<std::string> tokenize_command(const std::string& input); }