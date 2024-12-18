#include "objects.h"

void player::act(int n, std::vector<std::vector<std::string>> objects_position)
{
    if (n == 1)
    {
        int bullet_x = x;
        int bullet_y = y - 1;
        mvaddch(bullet_y, bullet_x, ACS_LANTERN);
        for (int i = bullet_y; i > min_y - 1; i--)
        {
            if (objects_position[i][bullet_x] == "wall")
            {
                break;
            }
            mvaddch(i, bullet_x, ACS_LANTERN);
            refresh();
            napms(80);
            mvaddch(i, bullet_x, ' ');
        }
    }

    if (n == 2)
    {
        int bullet_x = x;
        int bullet_y = y + 1;
        mvaddch(bullet_y, bullet_x, ACS_LANTERN);
        for (int i = bullet_y; i < max_y + 1; i++)
        {
            if (objects_position[i][bullet_x] == "wall")
            {
                break;
            }
            mvaddch(i, bullet_x, ACS_LANTERN);
            refresh();
            napms(80);
            mvaddch(i, bullet_x, ' ');
        }
    }

    if (n == 3)
    {
        int bullet_x = x + 1;
        int bullet_y = y;
        mvaddch(bullet_y, bullet_x, ACS_LANTERN);
        for (int i = bullet_x; i < max_x; i++)
        {
            if (objects_position[bullet_y][i] == "wall")
            {
                break;
            }
            mvaddch(bullet_y, i, ACS_LANTERN);
            refresh();
            napms(25);
            mvaddch(bullet_y, i, ' ');
        }
    }

    if (n == 4)
    {
        int bullet_x = x - 1;
        int bullet_y = y;
        mvaddch(bullet_y, bullet_x, ACS_LANTERN);
        for (int i = bullet_x; i > min_x; i--)
        {
            if (objects_position[bullet_y][i] == "wall")
            {
                break;
            }
            mvaddch(bullet_y, i, ACS_LANTERN);
            refresh();
            napms(25);
            mvaddch(bullet_y, i, ' ');
        }
    }
}

void player::move(std::vector<std::vector<std::string>> objects_position)
{
    keypad(stdscr, TRUE);
    curs_set(0);
    x = 37;
    y = 14;
    min_x = 36;
    max_x = 93;
    min_y = 2;
    max_y = 14;

    mvaddch(y, x, ACS_BLOCK);
    refresh();
    int ch;
    int begin_coordinate;

    while ((ch = getch()) != 'q')
    {
        switch ((ch))
        {
        case KEY_UP:
            begin_coordinate = y;
            y = y > min_y ? y - 1 : y;
            if (objects_position[y][x] == "wall")
            {
                y = begin_coordinate;
                break;
            }
            mvaddch(begin_coordinate, x, ' ');
            mvaddch(y, x, ACS_BLOCK);
            break;

        case KEY_DOWN:
            begin_coordinate = y;
            y = y < max_y ? y + 1 : y;
            if (objects_position[y][x] == "wall")
            {
                y = begin_coordinate;
                break;
            }
            mvaddch(begin_coordinate, x, ' ');
            mvaddch(y, x, ACS_BLOCK);
            break;

        case KEY_RIGHT:
            begin_coordinate = x;
            x = x < max_x ? x + 1 : x;
            if (objects_position[y][x] == "wall")
            {
                x = begin_coordinate;
                break;
            }
            mvaddch(y, begin_coordinate, ' ');
            mvaddch(y, x, ACS_BLOCK);
            break;

        case KEY_LEFT:
            begin_coordinate = x;
            x = x > min_x ? x - 1 : x;
            if (objects_position[y][x] == "wall")
            {
                x = begin_coordinate;
                break;
            }
            mvaddch(y, begin_coordinate, ' ');
            mvaddch(y, x, ACS_BLOCK);
            break;

        case 'w':
            act(1, objects_position);
            break;

        case 's':
            act(2, objects_position);
            break;

        case 'd':
            act(3, objects_position);
            break;

        case 'a':
            act(4, objects_position);
            break;

        default:
            mvaddch(y, x, ' ');
            mvaddch(y, x, ACS_BLOCK);
            break;
            refresh();
        }
    }
}