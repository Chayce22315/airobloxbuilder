#include "airo_native.hpp"
#include <algorithm>
#include <cctype>
namespace airo { health_result health(){return {1,"airo native online"};} std::string normalize_request(const std::string& text){auto a=text.find_first_not_of(" \t\r\n");if(a==std::string::npos)return{};auto b=text.find_last_not_of(" \t\r\n");auto v=text.substr(a,b-a+1);std::transform(v.begin(),v.end(),v.begin(),[](unsigned char c){return(char)std::tolower(c);});return v;} }