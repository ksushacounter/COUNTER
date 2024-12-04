#include "music.h"
#include "convert_factory.h"
#include "format_factory.h"
#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <memory>
#include <sstream>

int main(int argc, char* argv[])
{
    std::string txt_path = argv[1];  
    std::string output_path = argv[2];  

    std::vector<std::unique_ptr<FORMAT>> files;

    for (int i = 3; i < argc; ++i)
    {
        std::string path = argv[i];
        auto file = format_factory::create_format(path);
        files.push_back(std::move(file));
    }

    std::ifstream txt_file(txt_path);
    std::string line;
    std::vector<Comand> comands;

    if (!txt_file.is_open())
    {
        std::cerr << "Failed to open config file: " << txt_path << std::endl;
        return 1;
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
            converter->convert(files, comands, output_path, i);
        }
        files[0]->save(output_path);


    }
    catch (const std::exception& bad)
    {
        std::cerr << "Error: " << bad.what() << std::endl;
        return 1;
    }

    return 0;
}
