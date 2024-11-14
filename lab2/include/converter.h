#pragma once
#include <vector>

class converter {
public:
    virtual ~converter() = default;

    virtual void convert(std::vector<char>& data, int byteRate, int start_sec, int end_sec) = 0;
};


class mute : public converter {
public:
    void convert(std::vector<char>& audioData, int byteRate, int startSecond, int endSecond) override;
};
