#include "factory.h"
#include "converter.h"
#include <stdexcept>
#include <memory>

std::unique_ptr<converter> converter_factory::create_converter(const std::string& type){
if(type == "mute"){
    return std::make_unique<mute>();
}

else if(type == "bass_boost"){
    return std::make_unique<bass_boost>();
}

else if(type == "mix"){
    return std::make_unique<mix>();
}

else{
    throw std::invalid_argument("unknow converter:(");
}
}