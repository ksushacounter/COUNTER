#include "objects.h"
#include <iostream>

player::player(int x, int y, int min_x, int min_y, int max_x, int max_y)
    : x(x), y(y), min_x(min_x), min_y(min_y), max_x(max_x), max_y(max_y) {};

void player::display()
{
    mvaddch(y, x, ACS_BLOCK);
}

void player::act(int key)
{
    int bullet_x = x;
    int bullet_y = y;

    if (bullet_x >= min_x && bullet_x <= max_x && bullet_y >= min_y && bullet_y <= max_y)
    {
        bullets.push_back(new bullet(bullet_x, bullet_y, key, min_x, min_y, max_x, max_y));
        std::cout << 20 << std::endl;

    }
}

void player::update(std::vector<std::vector<std::string>> objects_position, int ch)
{

    int begin_coordinate;

    switch (ch)
    {

    case KEY_UP:
        begin_coordinate = y;
        y = y > min_y ? y - 1 : y;
        if (objects_position[y][x] == "wall")
        {
            y = begin_coordinate;
            break;
        }
        break;

    case KEY_DOWN:
        begin_coordinate = y;
        y = y < max_y ? y + 1 : y;
        if (objects_position[y][x] == "wall")
        {
            y = begin_coordinate;
            break;
        }
        break;

    case KEY_RIGHT:
        begin_coordinate = x;
        x = x < max_x ? x + 1 : x;
        if (objects_position[y][x] == "wall")
        {
            x = begin_coordinate;
            break;
        }
        break;

    case KEY_LEFT:
        begin_coordinate = x;
        x = x > min_x ? x - 1 : x;
        if (objects_position[y][x] == "wall")
        {
            x = begin_coordinate;
        }
        break;

    case 'w':
        act(1);
        break;

    case 's':
        act(2);
        break;

    case 'd':
        act(3);
        break;

    case 'a':
        act(4);
        break;

    default:
        break;
    }
}

bullet::bullet(int x, int y, int key, int min_x, int min_y, int max_x, int max_y)
    : x(x), y(y), key(key), min_x(min_x), min_y(min_y), max_x(max_x), max_y(max_y), is_active(true) {}

void bullet::display()
{

    mvaddch(y, x, ACS_LANTERN);
}

void bullet::update(std::vector<std::vector<std::string>> objects_position, int ch)
{
    switch (key)
    {
    case 1:
        if (y < max_y && y > min_y &&objects_position[y - 1][x] != "wall")
        {
            y -= 1;
            std::cout << y << ' ' << min_y << ' ' <<max_y << objects_position[y - 1][x] << std::endl;
        }
        else
        {
            is_active = false;
        }
        break;
    case 2:
        if (y < max_y && y > min_y && objects_position[y + 1][x] != "wall")
        {
            y += 1;
        }
        else
        {
            is_active = false;
        }
        break;
    case 3:
        if (x < max_x && x > min_x && objects_position[y][x + 1] != "wall")
        {
            x += 1;
        }
        else
        {
            is_active = false;
        }
        break;
    case 4:
        if (x > min_x && x < max_x && objects_position[y][x - 1] != "wall")
        {
            x -= 1;
        }
        else
        {
            is_active = false;
        }
        break;
    }
}
