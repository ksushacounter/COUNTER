#pragma once
#include <vector>
#include <string>
#include "music.h"

class converter {
public:
    virtual ~converter() = default;

    virtual void convert(std::vector<class WAV>& input_WAV, std::vector<Comand> comands, std::string output_path, int i) = 0;
};


class mute : public converter {
public:
    void convert(std::vector<class WAV>& input_WAV, std::vector<Comand> comands, std::string output_path, int i) override;
};

class bass_boost : public converter {
    public:
    void convert(std::vector<class WAV>& input_WAV, std::vector<Comand> comands, std::string output_path, int i) override;
};

class mix : public converter {
    public:
    void convert(std::vector<class WAV>& input_WAV, std::vector<Comand> comands, std::string output_path, int i) override;
};