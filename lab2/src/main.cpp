#include "music.h"
#include "factory.h"
#include <string>
#include <iostream>

int main()
{
    WAV wav("C:\\Users\\garku\\git\\lab2\\funkorama.wav");
    try
    {
        std::vector<char> &data = wav.get_data();
        int byteRate = wav.get_header().byteRate;
        int sampleRate = wav.get_header().sampleRate;

        std::unique_ptr<converter> converter = converter_factory::create_converter("bass_boost");
        converter->convert(data, byteRate, sampleRate, 1, 5, 10);
        
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

