#pragma once
#include <vector>
#include <string>
#include <curses.h>
#include <objects.h>
#include <memory>

class engine
{
private:
    std::vector<std::vector<std::string>> objects_position;
    player *current_player;

public:
    engine();
    ~engine();
    void update(int ch);
    void display();
    void run();
    int x = 37;
    int y = 14;
    int min_x = 36;
    int max_x = 93;
    int min_y = 2;
    int max_y = 14;
};
