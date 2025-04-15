#pragma once
#include <memory>
#include "objects.h"

class engine {
private:
    player current_player;
    std::vector<std::unique_ptr<bullet>> bullets; 
    std::vector<std::vector<std::string>> objects_position; 

public:
    engine(bool is_running, player current_player);
    bool is_running; 
    void processInput(); 
    void update();       
    void render();       
    void run();         
};
