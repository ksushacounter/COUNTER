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

class FORMAT
{
public:
    virtual ~FORMAT() = default;
    virtual void save(const std::string &output_file) = 0;

    virtual const Header &get_header() const = 0;
    virtual std::vector<int16_t> &get_data() = 0;
    virtual void load(const std::string &input_file) = 0;
    virtual int get_start_sample(int start_sec) = 0;
    virtual int get_end_sample(int end_sec) = 0;
};

class WAV : public FORMAT{
private:
    Header header;
    Subchunk data_chunk;
    std::vector<int16_t> data;
    void load(const std::string& input_file);

public: 
    WAV(const std::string& input_file);
    void save(const std::string& output_file) override;
    const Header& get_header() const override{
         return header; 
    }
    
    std::vector<int16_t>& get_data() override{ 
        return data; 
    }
    int get_start_sample(int start_sec) override{
        int start_sample = start_sec * get_header().sampleRate;
        return start_sample;
    }
    int get_end_sample(int end_sec) override{
        int end_sample = end_sec * get_header().sampleRate;
        return end_sample;
    }
};

