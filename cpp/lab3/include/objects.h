#pragma once
#include <curses.h>
#include <vector>
#include <string>

class object
{
public:
    void virtual update(std::vector<std::vector<std::string>> objects_position, int key) = 0;
    void virtual display() = 0;
    void virtual act(int key) = 0;
};

class bullet : public object
{
private:
    int key;
    int max_x, max_y;
    int min_x, min_y;
public:
    bullet(int y, int x, int key, int min_x, int min_y, int max_x, int max_y);
    void update(std::vector<std::vector<std::string>> objects_position, int key) override;
    void display() override;
    void act(int key) override {};
    bool is_active;
    int x, y;


};


class player : public object
{
private:
    int x, y;
    int max_x, max_y;
    int min_x, min_y;
    
public:
    player(int x, int y, int min_x, int min_y, int max_x, int max_y);
    void update(std::vector<std::vector<std::string>> objects_position, int key) override;
    void display() override;
    void act(int key) override;
    std::vector<bullet*> bullets;

};

