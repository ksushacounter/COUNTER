#include "factory.h"
#include "converter.h"
#include <stdexcept>
#include <memory>

std::unique_ptr<converter> converter_factory::create_converter(const std::string& type){
if(type == "mute"){
    return std::make_unique<mute>();
}
else{
    throw std::invalid_argument("unknow converter:(");
}
}
