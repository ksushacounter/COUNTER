#pragma once
#include <vector> 
#include <string>
#include <stdint.h>

struct Header{
    char id[4];
    uint32_t size;
    char format[4];
    char subchunk1ID[4];      
    uint32_t subchunk1Size;   
    uint16_t audioFormat;      
    uint16_t numChannels;     
    uint32_t sampleRate;    //частота дискретизации  
    uint32_t byteRate;      //байты в секунду
    uint16_t blockAlign;  
    uint16_t bitsPerSample;
};
struct Subchunk{
    uint32_t subchunk2Id;
    uint32_t subchunk2Size;   //размер файла
};
struct Comand{
    std::string name;
    int parametr1;
    int parametr2;
};

class WAV{
private:
    Header header;
    Subchunk data_chunk;
    std::vector<int16_t> data;
    void load(const std::string& input_file);

public: 
    WAV(const std::string& input_file);
    void save(const std::string& output_file);
    const Header& get_header() const {
         return header; 
    }
    
    std::vector<int16_t>& get_data(){ 
        return data; 
    }
};

