#include <iostream>
#include <curses.h>
#include <string>
#include <vector>
#include <random>
#include <start_game.h>

void start::intro()
{
    if (has_colors())
    {
        start_color();
        init_pair(1, COLOR_RED, COLOR_BLACK);
        init_pair(2, COLOR_GREEN, COLOR_BLACK);
        init_pair(3, COLOR_RED, COLOR_BLACK);
        init_pair(4, COLOR_CYAN, COLOR_WHITE);
    }

    attron(COLOR_PAIR(1));
    curs_set(0);
    mvprintw(5, 50, "$produced by counter$");
    refresh();
    napms(1000);
    mvprintw(7, 52, "press any button");
    getch();
    clear();
    mvprintw(5, 50, "are you ready?");
    refresh();
    napms(1000);
    mvprintw(7, 48, "press any button");
    getch();
    refresh();
    clear();
    mvprintw(5, 60, "GO");
    refresh();
    napms(1000);
    mvprintw(7, 54, "press any button");
    getch();
    refresh();
    attroff(COLOR_PAIR(1));

    attron(COLOR_PAIR(2));
    mvprintw(3, 40, "$$$$$");
    refresh();
    napms(200);
    mvprintw(2, 10, "$$$$$");
    refresh();
    napms(200);
    mvprintw(19, 100, "$$$$$");
    refresh();
    napms(150);
    mvprintw(5, 44, "$$$$$");
    refresh();
    napms(100);
    mvprintw(13, 15, "$$$$$");
    refresh();
    napms(100);
    mvprintw(3, 70, "$$$$$");
    refresh();
    napms(100);
    mvprintw(10, 75, "$$$$$");
    refresh();
    napms(1000);
    attroff(COLOR_PAIR(2));

    attron(COLOR_PAIR(3));
    mvprintw(2, 30, "$$$$$");
    refresh();
    napms(150);
    mvprintw(10, 100, "$$$$$");
    refresh();
    napms(150);
    mvprintw(9, 44, "$$$$$");
    refresh();
    napms(150);
    mvprintw(9, 60, "$$$$$");
    refresh();
    napms(150);
    mvprintw(9, 14, "$$$$$");
    refresh();
    napms(150);
    mvprintw(8, 90, "$$$$$");
    refresh();
    napms(150);
    mvprintw(10, 73, "$$$$$");
    refresh();
    napms(150);
    mvprintw(7, 90, "$$$$$");
    refresh();
    napms(150);
    mvprintw(5, 14, "$$$$$");
    refresh();
    napms(150);
    mvprintw(8, 40, "$$$$$");
    refresh();
    mvprintw(10, 44, "$$$$$");
    refresh();
    napms(150);
    mvprintw(13, 20, "$$$$$");
    refresh();
    napms(150);
    mvprintw(3, 78, "$$$$$");
    refresh();
    napms(150);
    mvprintw(5, 75, "$$$$$");
    refresh();
    napms(800);
    attroff(COLOR_PAIR(3));

    for (int i = 0; i < 15; i++)
    {
        bkgd(COLOR_PAIR(4));
        refresh();
        napms(80);
        bkgd(COLOR_PAIR(1));
        refresh();
        napms(80);
    }

    clear();
}

std::vector<std::vector<std::string>> start::map()
{
    int startY = 1;
    int startX = 35;
    int width = 60;
    int height = 15;
    std::vector<std::vector<std::string>> objects_position(height + startY, std::vector<std::string>(width + startX, "false"));

    // рамка
    mvaddch(startY, startX, ACS_ULCORNER);
    for (int i = 1; i < width - 1; ++i)
    {
        mvaddch(startY, startX + i, ACS_HLINE);
    }
    mvaddch(startY, startX + width - 1, ACS_URCORNER);

    for (int i = 1; i < height - 1; ++i)
    {
        mvaddch(startY + i, startX, ACS_VLINE);
        mvaddch(startY + i, startX + width - 1, ACS_VLINE);
    }

    mvaddch(startY + height - 1, startX, ACS_LLCORNER);
    for (int i = 1; i < width - 1; ++i)
    {
        mvaddch(startY + height - 1, startX + i, ACS_HLINE);
    }
    mvaddch(startY + height - 1, startX + width - 1, ACS_LRCORNER);

    // стены
    int wail_length = height - 4;
    for (int j = 0; j < wail_length; ++j)
    {
        mvaddch(height - 2 - j, startX + 5, ACS_VLINE);
        objects_position[height - 2 - j][startX + 5] = "wall";
    }

    wail_length = 15;
    for (int j = 0; j < wail_length; ++j)
    {
        mvaddch(height - 5, startX + 15 + j, ACS_HLINE);
        objects_position[height - 5][startX + 15 + j] = "wall";
        mvaddch(height - 7, startX + 15 + j, ACS_HLINE);
        objects_position[height - 7][startX + 15 + j] = "wall";
        mvaddch(height - 10, startX + 40 + j, ACS_HLINE);
        objects_position[height - 10][startX + 40 + j] = "wall";
        mvaddch(height - 10, startX + 15 + j, ACS_HLINE);
        objects_position[height - 10][startX + 15 + j] = "wall";
        mvaddch(height - 13, startX + 10 + j, ACS_HLINE);
        objects_position[height - 13][startX + 10 + j] = "wall";
    };

    wail_length = height / 2;
    for (int j = 0; j < wail_length; ++j)
    {
        mvaddch(height - 10 + j, startX + 15, ACS_VLINE);
        objects_position[height - 10 + j][startX + 15] = "wall";
        mvaddch(height - 7 + j, startX + 40, ACS_VLINE);
        objects_position[height - 7 + j][startX + 40] = "wall";
        mvaddch(height - 11 + j, startX + 55, ACS_VLINE);
        objects_position[height - 11 + j][startX + 55] = "wall";
    }


    refresh();
    attroff(COLOR_PAIR(3));
    return objects_position;
}
