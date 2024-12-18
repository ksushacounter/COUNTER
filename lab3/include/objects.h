#pragma once
#include <curses.h>
#include <vector>
#include <string>

class object
{
public:
    void virtual act(int n, std::vector<std::vector<std::string>> objects_position) = 0;
    void virtual move(std::vector<std::vector<std::string>> objects_position) = 0;
};

class player : public object
{
public:
    void act(int n, std::vector<std::vector<std::string>> objects_position) override;
    void move(std::vector<std::vector<std::string>> objects_position) override;
    int x;
    int y;
    int max_x;
    int max_y;
    int min_x;
    int min_y;
};
