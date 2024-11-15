#include "music.h"
#include "factory.h"
#include <string>
#include <iostream>

int main()
{
    WAV wav("C:\\Users\\garku\\git\\lab2\\funkorama.wav");
    try
    {
        // std::ifstream file("input.txt");
        // if(!file){
        //     throw std::runtime_error("bad input file:(");
        // }
        // file.read(data.data(), header.subchunk2Size);
        // file.close();

        std::vector<char> &data = wav.get_data();
        int byteRate = wav.get_header().byteRate;

        std::cout << wav.get_header().id << std::endl; 
        std::cout << wav.get_header().size << std::endl; 
        std::cout << wav.get_header().format << std::endl; 
        std::cout << wav.get_header().subchunk1ID << std::endl; 
        std::cout << wav.get_header().subchunk1Size << std::endl; 
        std::cout << wav.get_header().audioFormat << std::endl; 
        std::cout << wav.get_header().numChannels << std::endl; 
        std::cout << wav.get_header().sampleRate << std::endl; 
        std::cout << wav.get_header().byteRate << std::endl; 
        std::cout << wav.get_header().blockAlign << std::endl; 
        std::cout << wav.get_header().bitsPerSample << std::endl; 
        

        std::unique_ptr<converter> converter = converter_factory::create_converter("bass_boost");
        converter->convert(data, byteRate, 1, 5, 10);
        
        wav.save("C:\\Users\\garku\\git\\lab2\\my.wav");
        std::cout << "Done" << std::endl;
    }
    catch (const std::exception &bad)
    {
        std::cerr << "Error: " << bad.what() << std::endl;
        return 1;
    }

    return 0;
}

