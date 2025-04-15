#include "game_engine.h"
#include "objects.h"
#include <curses.h>
#include <vector>
#include <memory>

engine::engine(bool is_running, player current_player)
    : is_running(true), current_player(player(37, 14, objects_position)) {}

void engine::processInput()
{
    keypad(stdscr, TRUE);
    curs_set(0);
    int ch = getch();

    mvaddch(14, 37, ACS_BLOCK);
    refresh();
    switch (ch)
    {
    case KEY_UP:
        current_player.move(0, -1);
        break;
        refresh();
    }

    if (ch == 'q')
    {
        is_running = false;
        return;
    }
    // current_player.handle_input(ch, bullets);
    
}

void engine::update()
{

    for (auto &bullet : bullets)
    {
        bullet->move(0, 0);
    }

    for (auto it = bullets.begin(); it != bullets.end();)
    {
        if (!(*it)->is_alive())
        {
            it = bullets.erase(it);
        }
        else
        {
            ++it;
        }
    }
}

void engine::render()
{
    current_player.draw();

    for (auto &bullet : bullets)
    {
        bullet->draw();
    }
}

void engine::run()
{
    while (is_running)
    {
        processInput();
        update();
        render();
        napms(50);
    }
    endwin();
}
