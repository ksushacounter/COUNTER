#pragma once
#include "converter.h"
#include <memory>

class converter_factory{
public:
    static std::unique_ptr<converter> create_converter(const std::string& type);
};