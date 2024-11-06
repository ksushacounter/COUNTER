#include <fstream>
#include <iostream>
#include <music.h>
#include <cstring>

wav::wav(const std::string& input_file){
    load(input_file);
}

void wav::load(const std::string& input_file){
    std::ifstream file(input_file, std::ios::binary);
    if(!file){
        throw std::runtime_error("bad input file:(");
    }
    file.read(reinterpret_cast<char*>(&header), sizeof(Header));
    if (std::strncmp(header.id, "RIFF", 4) != 0 || std::strncmp(header.format, "WAVE", 4) != 0) {
        throw std::runtime_error("bad waf:(");
    }
    data.resize(header.subchunk2Size);
    file.read(data.data(), header.subchunk2Size);
    file.close();
}

void wav::save(std::string& output_file){
    std::ofstream file(output_file, std::ios::binary);
    if(!file){
        throw std::runtime_error("bad outpit:(");
    }
    file.write(reinterpret_cast<const char*>(&header), sizeof(Header));
    file.write(data.data(), data.size());
    file.close();

}


