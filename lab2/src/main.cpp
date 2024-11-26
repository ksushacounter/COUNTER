#include "music.h"
#include "factory.h"
#include <string>
#include <iostream>
#include <fstream>
#include <iostream>
#include <sstream>

int main()
{
    int number_files;
    std::vector<WAV> input_WAV;
    std::cin >> number_files;
    for (int i = 0; i < number_files; i++)
    {
        std::string path;
        std::cin >> path;
        WAV wav(path);
        input_WAV.emplace_back(wav);
    }
    std::string output_path;
    std::cin >> output_path;

    std::string txt_path;
    std::cin >> txt_path;

    std::ifstream txt_file(txt_path);
    std::string line;
    std::vector<Comand> comands;

    if (!txt_file.is_open())
    {
        throw std::runtime_error("Failed to open config file: " + txt_path);
    }

    Comand comand;
    try
    {
        int count = 0;
        while (std::getline(txt_file, line))
        {
            std::stringstream ss(line);

            ss >> comand.name >> comand.parametr1 >> comand.parametr2;

            comands.push_back(comand);
            count++;
        }
        txt_file.close();
        for (int i = 0; i < count; i++)
        {
            std::unique_ptr<converter> converter = converter_factory::create_converter(comands[i].name);
            converter->convert(input_WAV, comands, output_path, i);
        }
    }
    catch (const std::exception &bad)
    {
        std::cerr << "Error: " << bad.what() << std::endl;
        return 1;
    }
    return 0;
}

// int main()
// {
//     WAV wav("C:\\Users\\garku\\git\\lab2\\funkorama.wav");
//     WAV wav2("C:\\Users\\garku\\git\\lab2\\severe_tire_damage.wav");

//     try
//     {
//         std::vector<char> &data = wav.get_data();
//         std::vector<char> &data2 = wav2.get_data();

//         int byteRate = wav.get_header().byteRate;
//         int sampleRate = wav.get_header().sampleRate;

//         std::unique_ptr<converter> converter = converter_factory::create_converter("bass_boost");
//         converter->convert(data, data2, byteRate, sampleRate, 1, 5, 150);

//         wav.save("C:\\Users\\garku\\git\\lab2\\my.wav");
//         std::cout << "Done" << std::endl;
//     }
//     catch (const std::exception &bad)
//     {
//         std::cerr << "Error: " << bad.what() << std::endl;
//         return 1;
//     }
//     return 0;
// }