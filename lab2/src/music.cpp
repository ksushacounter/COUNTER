#include <fstream>
#include <iostream>
#include "music.h"
#include <cstring>
#include <string>

WAV::WAV(const std::string &input_file)
{
    load(input_file);
}

void WAV::load(const std::string &input_file)
{
    std::ifstream file(input_file, std::ios::binary);
    if (!file)
    {
        throw std::runtime_error("bad input file:(");
    }
    file.read(reinterpret_cast<char *>(&header), sizeof(Header));
    for (;;)
    {
        file.read(reinterpret_cast<char *>(&data_chunk), sizeof(Subchunk));
        std::cout << data_chunk.subchunk2Id << std::endl << data_chunk.subchunk2Size << std::endl; 
        if (data_chunk.subchunk2Id == 0x61746164)
        {
            data.resize(data_chunk.subchunk2Size);
            file.read(data.data(), data_chunk.subchunk2Size);
            file.close();
            break;
        }
        else
        {
            file.seekg(data_chunk.subchunk2Size, std::ios_base::cur);
        }
    }
}

    void WAV::save(const std::string &output_file)
    {
        std::ofstream file(output_file, std::ios::binary);
        if (!file)
        {
            throw std::runtime_error("bad outpit:(");
        }
        file.write(reinterpret_cast<const char *>(&header), sizeof(Header));
        file.write(reinterpret_cast<const char *>(&data_chunk), sizeof(Subchunk));
        file.write(data.data(), data.size());
        file.close();
    }
