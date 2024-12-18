#include <iostream>
#include <string>
#include <start_game.h>
#include <curses.h>
#include <objects.h>


int main()
{
    initscr();
    cbreak();
    noecho();

    start start_game;
    player player;
    start_game.intro();
    std::vector<std::vector<std::string>> objects_position = start_game.map();
    player.move(objects_position);
}
