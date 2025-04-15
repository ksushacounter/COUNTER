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
        throw std::runtime_error("Failed to open input file: " + input_file);
    }

    file.read(reinterpret_cast<char *>(&header), sizeof(Header));

    while (file.read(reinterpret_cast<char *>(&data_chunk), sizeof(Subchunk)))
    {
        uint32_t data_word = 0x61746164;
        if (data_chunk.subchunk2Id == data_word) 
        {
            data.resize(data_chunk.subchunk2Size / sizeof(int16_t));
            file.read(reinterpret_cast<char *>(data.data()), data_chunk.subchunk2Size);
            break;
        }
        else
        {
            file.seekg(data_chunk.subchunk2Size, std::ios_base::cur);
        }
    }

    if (file.fail() && !file.eof())
    {
        throw std::runtime_error("Error while reading the file: " + input_file);
    }

    file.close();
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

    
    file.write(reinterpret_cast<char*> (data.data()), data.size() * sizeof(uint16_t));
    file.close();
}
