
#include "converter.h"
#include <fstream>
#include <algorithm>
#include <iostream>

void mute::convert(std::vector<char>& data, int byteRate, int start_sec, int end_sec){
    int start_byte = start_sec * byteRate;
    int end_byte = end_sec * byteRate;
    if(start_byte < 0 || end_byte > data.size() || start_byte >= end_byte){
        throw std::invalid_argument ("bad range:(");
    }
    std::fill(data.begin() + start_byte, data.begin() + end_byte, 0);
    std::cout << "done2" << std::endl;
}

void bass_boost::convert(std::vector<char>& data, int byteRate, int start_sec, int end_sec, int gain){
    int cutoffFreq = 250;
    double boost = gain / 100;

    for (size_t i = 1; i < data.size(); i++) {
        if (data[i] < 0) {
            data[i] = static_cast<int16_t>(data[i] * gain);
        } else {
            data[i] = static_cast<int16_t>(data[i] * gain);
        }
    }
}
