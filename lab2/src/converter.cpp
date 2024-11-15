
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
    int start_byte = start_sec * byteRate;
    int end_byte = end_sec * byteRate;
    double double_byte_rate = 44100.0;
    if(start_byte < 0 || end_byte > data.size() || start_byte >= end_byte){
        throw std::invalid_argument ("bad range:(");
    }
    fftw_complex *in = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * data.size());
    fftw_complex *out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * data.size());
    fftw_plan plan_forward = fftw_plan_dft_1d(data.size(), in, out, FFTW_FORWARD, FFTW_ESTIMATE);

    for(int i = 0; i < data.size(); i++){
        in[i][0] = data[i];
        in[i][1] = 0;
    }

    fftw_execute(plan_forward);
    double step = double_byte_rate / data.size(); //интервал между частотами
    for(int i = 0; i < data.size(); i++){
        double freq = step * i;
        if(freq <= 250){
            in[i][0] *= gain;
            in[i][1] *= gain;
        }
    }
    fftw_plan plan_back = fftw_plan_dft_1d(data.size(), out, in, FFTW_FORWARD, FFTW_ESTIMATE);
    fftw_execute(plan_back);
    for(int i = 0; i < data.size(); i++){
        data[i] = static_cast<uint16_t>(in[i][0] / data.size()); 
    }

    fftw_destroy_plan(plan_forward);
    fftw_destroy_plan(plan_back);
    fftw_free(in);
    fftw_free(out);
}