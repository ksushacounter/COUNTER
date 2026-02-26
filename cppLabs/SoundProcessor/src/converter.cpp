#include "converter.h"
#include "music.h"
#include <vector>
#include <iostream>
#include <cmath>
#include <stdint.h>
#include <string>
#include <memory>

void mute::convert(std::vector<std::unique_ptr<FORMAT>>& files, std::vector<Comand>& comands, int i) {
    
    FORMAT& file = *files[0]; 
    std::vector<int16_t>& data = file.get_data();
    int sampleRate = file.get_header().sampleRate;

    int start_sec = comands[i].parametr1;
    int end_sec = comands[i].parametr2;
    int start_sample = start_sec * sampleRate;
    int end_sample = end_sec * sampleRate;

    std::fill(data.begin() + start_sample, data.begin() + end_sample, 0);
    // file.save(output_path);
    std::cout << "Done:)" << std::endl;
}


// void bass_boost::convert(std::vector<char>& data, int byteRate, int start_sec, int end_sec, int gain){
//     int start_byte = start_sec * byteRate;
//     int end_byte = end_sec * byteRate;
//     double double_byte_rate = 44100.0;
//     if(start_byte < 0 || end_byte > data.size() || start_byte >= end_byte){
//         throw std::invalid_argument ("bad range:(");
//     }
//     fftw_complex *in = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * data.size());
//     fftw_complex *out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * data.size());
//     fftw_plan plan_forward = fftw_plan_dft_1d(data.size(), in, out, FFTW_FORWARD, FFTW_ESTIMATE);

//     for(int i = 0; i < data.size(); i++){
//         in[i][0] = data[i];
//         in[i][1] = 0;
//     }

//     fftw_execute(plan_forward);
//     double step = double_byte_rate / data.size(); //интервал между частотами
//     for(int i = 0; i < data.size(); i++){
//         double freq = step * i;
//         if(freq <= 250){
//             in[i][0] *= gain;
//             in[i][1] *= gain;
//         }
//     }
//     fftw_plan plan_back = fftw_plan_dft_1d(data.size(), out, in, FFTW_FORWARD, FFTW_ESTIMATE);
//     fftw_execute(plan_back);
//     for(int i = 0; i < data.size(); i++){
//         data[i] = static_cast<uint16_t>(in[i][0] / data.size());
//     }

//     fftw_destroy_plan(plan_forward);
//     fftw_destroy_plan(plan_back);
//     fftw_free(in);
//     fftw_free(out);
// }


void bass_boost::convert(std::vector<std::unique_ptr<FORMAT>>& files, std::vector<Comand>& comands, int i) {
    if (files.empty()) {
        throw std::runtime_error("No files provided.");
    }

    FORMAT& file = *files[0];  

    std::vector<int16_t>& data = file.get_data();
    int byteRate = file.get_header().byteRate;
    int sampleRate = file.get_header().sampleRate;
    int gain = comands[i].parametr1;

    int start_sec = comands[i].parametr1;  
    int end_sec = comands[i].parametr2;    

    int start_sample = start_sec * byteRate / 2;  
    int end_sample = end_sec * byteRate / 2;

    if (start_sample < 0 || end_sample > data.size() || start_sample >= end_sample) {
        throw std::invalid_argument("Invalid sample range.");
    }

    size_t numSamples = data.size();
    const int filterSize = 101;  
    const int slice = 250;       

    std::vector<double> filter(filterSize);
    double normCutoff = static_cast<double>(slice) / sampleRate;

    for (int j = 0; j < filterSize; j++) {
        int n = j - filterSize / 2;
        if (n == 0) {
            filter[j] = 2 * normCutoff;
        } else {
            filter[j] = std::sin(2 * M_PI * normCutoff * n) / (M_PI * n);
        }
        filter[j] *= 0.54 - 0.46 * std::cos(2 * M_PI * j / (filterSize - 1));
    }

    double sum = 0.0;
    for (int j = 0; j < filterSize; j++) {
        sum += filter[j];
    }

    for (int j = 0; j < filterSize; j++) {
        filter[j] /= sum;
    }

    std::vector<int16_t> filteredSamples(data.begin(), data.end()); 
    for (size_t i = start_sample + filterSize / 2; i < end_sample - filterSize / 2; i++) {
        double filteredValue = 0.0;
        for (size_t j = 0; j < filterSize; j++) {
            filteredValue += data[i - filterSize / 2 + j] * filter[j];
        }
        filteredSamples[i] = static_cast<int16_t>(filteredValue * (1.0 + gain / 100.0));
    }

    std::copy(filteredSamples.begin(), filteredSamples.end(), data.begin());

    // file.save(output_path);
    std::cout << "Done:)" << std::endl;
}


void mix::convert(std::vector<std::unique_ptr<FORMAT>>& files, std::vector<Comand>& comands, int i)
{
    int second_file = comands[i].parametr1; 
    int start_sec = comands[i].parametr2;  

    FORMAT& file = *files[0];              
    FORMAT& file2 = *files[second_file - 1]; 

    std::vector<int16_t>& data = file.get_data();
    std::vector<int16_t>& data2 = file2.get_data();

    int sampleRate = file.get_header().sampleRate;

    int start_sample = start_sec * sampleRate;

    if (start_sample < 0)
    {
        throw std::invalid_argument("bad range:(");
    }

    for (int j = start_sample; j < data2.size() && j < data.size(); j++)
    {
        int32_t sum = static_cast<int32_t>(data[j]) + static_cast<int32_t>(data2[j - start_sample]);

        const int16_t uint16_t_border = 32767;
        if (sum > uint16_t_border)
        {
            data[j] = uint16_t_border;
        }
        else if (sum < -uint16_t_border)
        {
            data[j] = -uint16_t_border;
        }
        else
        {
            data[j] = static_cast<int16_t>(sum);
        }
    }

    // file.save(output_path);
    std::cout << "Done:)" << std::endl;
}
