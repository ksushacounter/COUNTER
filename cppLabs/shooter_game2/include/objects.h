#pragma once
#include <curses.h>
#include <vector>
#include <string>
#include <memory>


class object
{
public:
    // void virtual act() = 0;
    void virtual move(int direction_x, int direction_y) = 0;
    void virtual draw() = 0;
};

class bullet : public object
{
private:
    int x, y; 
    int direction_x, direction_y;                  
    bool is_active;            
    std::vector<std::vector<std::string>> objects_position; 
public:
    bullet(int x, int y, int direction_x, int direction_y, std::vector<std::vector<std::string>> objects_position);
    // void act() override {};     
    void move(int direction_x, int direction_y) override;        
    void draw() override;      
    bool is_alive() const { return is_active; }
};

class player : public object
{
private:
    int x, y;
    int max_x, max_y;
    int min_x, min_y;
    std::vector<std::vector<std::string>> objects_position;
public:
    player(int x, int y, std::vector<std::vector<std::string>> objects_position);
    // void act() override;
    void move(int direction_x, int direction_y) override;
    void draw() override;
    void handle_input(int ch, std::vector<std::unique_ptr<bullet>> &bullets);
};

