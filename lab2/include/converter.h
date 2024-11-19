#pragma once
#include <vector>

class converter {
public:
    virtual ~converter() = default;

    virtual void convert(std::vector<char>& data, int byteRate, int sampleRate, int start_sec, int end_sec) = 0;
};


class mute : public converter {
public:
    void convert(std::vector<char>& audioData, int byteRate, int sampleRate, int startSecond, int endSecond) override;
};

class bass_boost : public converter {
    public:
    void convert(std::vector<char>& data, int gain, int byteRate, int sampleRate, int startSecond, int endSecond);
}
