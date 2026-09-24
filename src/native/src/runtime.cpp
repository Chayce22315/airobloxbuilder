#include "airo_native/runtime.hpp"
#include <sstream>
namespace airo::native { Health health(){return {true,"airo native runtime online"};} std::vector<std::string> tokenize_command(const std::string& input){std::istringstream stream(input);std::vector<std::string> out;std::string part;while(stream>>part)out.push_back(part);return out;} }