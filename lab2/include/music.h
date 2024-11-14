#include <vector> 
#include <string>


struct Header{
    char id[4];
    int size;
    char format[4];
    char subchunk1ID[4];      
    int subchunk1Size;   
    int audioFormat;      
    int numChannels;     
    int sampleRate;    //частота дискретизации  
    int byteRate;      
    int blockAlign;  
    int bitsPerSample;
    char subchunk2Id[4];
    int subchunk2Size;
};

class wav{
private:
    Header header;
    std::vector<char> data;
    void load(const std::string& input_file);

public: 
    wav(const std::string& input_file);
    void mute(int start_sec, int end_sec);
    void save(std::string& output_file);

};
