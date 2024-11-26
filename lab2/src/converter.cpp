#include "converter.h"
#include "music.h"
#include <vector>
#include <iostream>
#include <cmath>
#include <stdint.h>
#include <string>

void mute::convert(std::vector<class WAV>& input_WAV, std::vector<Comand> comands, std::string output_path, int i)
{
    WAV& wav = input_WAV[0];
    std::vector<int16_t>& data = wav.get_data();
    int byteRate = wav.get_header().byteRate;
    int sampleRate = wav.get_header().sampleRate;

    int start_sec = comands[i].parametr1;
    int end_sec = comands[i].parametr2;
    int start_byte = start_sec * byteRate;
    int end_byte = end_sec * byteRate;

    std::cout << byteRate<< " " << sampleRate<< " " << start_sec<< " " << end_sec<< " " << start_byte << "  " << end_byte << std::endl;
    if (start_byte < 0 || end_byte > data.size() || start_byte >= end_byte)
    {
        throw std::invalid_argument("bad range:(");
    }
    std::fill(data.begin() + start_byte/2, data.begin() + end_byte/2, 0);
    wav.save(output_path);
    std::cout << "Done" << std::endl;
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

// void bass_boost::convert(std::vector<char>& data, int byteRate, int start_sec, int end_sec, int gain){
//     int slice = 250;
//     double boost = gain / 100;

//     for (size_t i = 1; i < data.size(); i++) {
//         if (data[i] < 0) {
//             data[i] = static_cast<int16_t>(data[i] * gain);
//         } else {
//             data[i] = static_cast<int16_t>(data[i] * gain);
//         }
//     }
// }

void bass_boost::convert(std::vector<class WAV>& input_WAV, std::vector<Comand> comands, std::string output_path, int i)
{
    int slice = 250;
    WAV& wav = input_WAV[0];
    std::vector<int16_t>& data = wav.get_data();
    int byteRate = wav.get_header().byteRate;
    int sampleRate = wav.get_header().sampleRate;
    int gain = comands[i].parametr1;
    
    size_t numSamples = data.size();


    int filterSize = 101;
    std::vector<double> filter(filterSize);

    // коэффициенты
    double normCutoff = static_cast<double>(slice) / sampleRate;
    for (int i = 0; i < filterSize; i++)
    {
        int n = i - filterSize / 2;
        if (n == 0)
        {
            filter[i] = 2 * normCutoff;
        }
        else
        {
            filter[i] = std::sin(2 * M_PI * normCutoff * n) / (M_PI * n);
        }
        // окно Хэмминга
        filter[i] *= 0.54 - 0.46 * std::cos(2 * M_PI * i / (filterSize - 1));
    }

    double sum = 0.0;
    for (double coeff : filter)
    {
        sum += coeff;
    }
    for (double &coeff : filter)
    {
        coeff /= sum;
    }

    std::vector<int16_t> filteredSamples(numSamples, 0);
    for (size_t i = filterSize / 2; i < numSamples - filterSize / 2; i++)
    {
        double filteredValue = 0.0;
        for (size_t j = 0; j < filterSize; j++)
        {
            filteredValue += data[i - filterSize / 2 + j] * filter[j];
        }
        filteredSamples[i] = static_cast<int16_t>(filteredValue * (1.0 + gain / 100.0));
    }
    std::copy(filteredSamples.begin(), filteredSamples.end(), data.begin());
    wav.save(output_path);
    std::cout << "Done" << std::endl;
}

void mix::convert(std::vector<class WAV>& input_WAV, std::vector<Comand> comands, std::string output_path, int i)
{
    int second_file = comands[i].parametr1;
    std::cout << second_file << std::endl;
    WAV& wav = input_WAV[0];
    WAV& wav2 = input_WAV[second_file - 1];

    std::vector<int16_t>& data = wav.get_data();
    std::vector<int16_t> data2 = wav2.get_data();

    int byteRate = wav.get_header().byteRate;
    int sampleRate = wav.get_header().sampleRate;

    int start_sec = comands[i].parametr2;
    int start_byte = start_sec * byteRate/2;

    if (start_byte < 0)
    {
        throw std::invalid_argument("bad range:(");
    }

    for (int j = start_byte/2; j < data2.size() && j < data.size(); j++)
    {
        int32_t sum = static_cast<int32_t>(data[j]) + static_cast<int32_t>(data2[j - start_byte / 2]);
        int uint16_t_border = 32767;
        if (data[j] > uint16_t_border)
        {
            data[j] = uint16_t_border;
        }
        if (data[j] < -uint16_t_border)
        {
            data[j] = -uint16_t_border;
        }
        else {
            data[j] = static_cast<int16_t> (sum);
        }
    }
    wav.save(output_path);
    std::cout << "Done" << std::endl;
}