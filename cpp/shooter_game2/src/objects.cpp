#include "objects.h"

player::player(int x, int y, std::vector<std::vector<std::string>> objects_position)
    : x(x), y(y), objects_position(objects_position) {}

void player::move(int direction_x, int direction_y)
{
    int new_x = x + direction_x;
    int new_y = y + direction_y;

    if ((objects_position)[new_y][new_x] != "wall")
    {
        mvaddch(y, x, ' '); 
        x = new_x;
        y = new_y;
        mvaddch(y, x, ACS_BLOCK); 
    }
    refresh();
}

void player::draw() 
{
    mvaddch(y, x, ACS_BLOCK); 
}

void player::handle_input(int ch, std::vector<std::unique_ptr<bullet>> &bullets)
{
    mvaddch(y,x, ACS_BLOCK);
    switch (ch)
    {
    case KEY_UP:
        move(0, -1);
        break;
    case KEY_DOWN:
        move(0, 1);
        break;
    case KEY_LEFT:
        move(-1, 0);
        break;
    case KEY_RIGHT:
        move(1, 0);
        break;
    case 'w':
        bullets.push_back(std::make_unique<bullet>(x, y - 1, 0, -1, objects_position));
        break;
    case 's':
        bullets.push_back(std::make_unique<bullet>(x, y + 1, 0, 1, objects_position));
        break;
    case 'a':
        bullets.push_back(std::make_unique<bullet>(x - 1, y, -1, 0, objects_position));
        break;
    case 'd':
        bullets.push_back(std::make_unique<bullet>(x + 1, y, 1, 0, objects_position));
        break;
    }
}

bullet::bullet(int x, int y, int direction_x, int direction_y, std::vector<std::vector<std::string>> objects_position)
    : x(x), y(y), direction_x(direction_x), direction_y(direction_y), is_active(true), objects_position(objects_position) {}

void bullet::move(int direction_x, int direction_y)
{
    int next_x, next_y;
    if (!is_active)
    {
        return;
    }

    else
    {
        next_x = x + direction_x;
        next_y = y + direction_y;
    }

    if ((objects_position)[next_y][next_x] == "wall")
    {
        is_active = false;
    }
    else
    {
        mvaddch(y, x, ' ');

        x = next_x;
        y = next_y;
    }

    refresh();
}

void bullet::draw()
{
    if (is_active)
    {
        mvaddch(y, x, ACS_LANTERN);
        refresh();
    }
}
