#pragma once
#include <vector>
#include <string>
#include "music.h"
#include <memory>

class converter {
public:
    virtual ~converter() = default;

    virtual void convert(std::vector<std::unique_ptr<FORMAT>>& files, std::vector<Comand>& comands, const std::string output_path, int i) = 0;
};


class mute : public converter {
public:
    void convert(std::vector<std::unique_ptr<FORMAT>>& files, std::vector<Comand>& comands, const std::string output_path, int i) override;
};

class bass_boost : public converter {
    public:
    void convert(std::vector<std::unique_ptr<FORMAT>>& files, std::vector<Comand>& comands, const std::string output_path, int i) override;
};

class mix : public converter {
    public:
    void convert(std::vector<std::unique_ptr<FORMAT>>& files, std::vector<Comand>& comands, const std::string output_path, int i) override;
};
