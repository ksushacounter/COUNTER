
#include "converter.h"
#include <fstream>
#include <algorithm>
#include <iostream>

void mute::convert(std::vector<char>& data, int byteRate, int sampleRate,int start_sec, int end_sec){
    int start_byte = start_sec * byteRate;
    int end_byte = end_sec * byteRate;
    if(start_byte < 0 || end_byte > data.size() || start_byte >= end_byte){
        throw std::invalid_argument ("bad range:(");
    }
    std::fill(data.begin() + start_byte, data.begin() + end_byte, 0);
    std::cout << "done2" << std::endl;
}

void bass_boost::convert(std::vector<char>& data, int byteRate, int sampleRate, int start_sec, int end_sec, int gain) {
    int cutoffFreq = 250;
    size_t numSamples = data.size() / 2;
    std::vector<int16_t> samples(numSamples);

    for (size_t i = 0; i < numSamples; i++) {
        samples[i] = static_cast<int16_t>(data[2 * i] | (data[2 * i + 1] << 8));
    }

    int filterSize = 101;  
    std::vector<double> filter(filterSize);

    //коэффициенты 
    double normCutoff = static_cast<double>(cutoffFreq) / sampleRate; 
    for (int i = 0; i < filterSize; i++) {
        int n = i - filterSize / 2; 
        if (n == 0) {
            filter[i] = 2 * normCutoff; 
        } else {
            filter[i] = std::sin(2 * M_PI * normCutoff * n) / (M_PI * n);
        }
        //окно Хэмминга
        filter[i] *= 0.54 - 0.46 * std::cos(2 * M_PI * i / (filterSize - 1));
    }

    double sum = 0.0;
    for (double coeff : filter) {
        sum += coeff;
    }
    for (double& coeff : filter) {
        coeff /= sum;
    }

    std::vector<int16_t> filteredSamples(numSamples, 0);
    for (size_t i = filterSize / 2; i < numSamples - filterSize / 2; i++) {
        double filteredValue = 0.0;
        for (size_t j = 0; j < filterSize; j++) {
            filteredValue += samples[i - filterSize / 2 + j] * filter[j];
        }
        filteredSamples[i] = static_cast<int16_t>(filteredValue * (1.0 + gain / 100.0)); 
    }

    for (size_t i = 0; i < numSamples; i++) {
        data[2 * i] = filteredSamples[i] & 0xFF;
        data[2 * i + 1] = (filteredSamples[i] >> 8) & 0xFF;
    }
}