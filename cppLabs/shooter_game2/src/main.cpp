#include <iostream>
#include <vector>
#include <memory>
#include <curses.h>
#include "game_engine.h"
#include "start_game.h"
#include "objects.h"

int main() {
    initscr();
    cbreak();
    noecho();
    curs_set(0);  

    start start_game;
    // start_game.intro();
    std::vector<std::vector<std::string>> objects_position = start_game.map();

    player current_player(37, 14, objects_position);
    engine game_engine(true, current_player);

    while (true) {
        game_engine.processInput();
        // game_engine.update();
        // game_engine.render();

        if (!game_engine.is_running) {
            break;
        }

        napms(50);
    }

    endwin();
    return 0;
}
