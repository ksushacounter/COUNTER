#include <iostream>
#include <string>
#include <curses.h>
#include <game_engine.h>

int main()
{
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE); 


    engine engine;
    engine.run();
}
