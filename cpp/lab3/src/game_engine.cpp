#include <game_engine.h>
#include <start_game.h>
#include <curses.h>
#include <objects.h>
#include <iostream>
#include <algorithm>




engine::engine()
{
    current_player = new player(x, y, min_x, min_y, max_x, max_y);
    
}

engine::~engine() {
        delete current_player;
        for (auto bullet : current_player->bullets) {
            delete bullet;
        }
        endwin();
    }

void engine::display()
{
    current_player->display();
    for(int i = 0 ; i < current_player->bullets.size(); i++)
        {
            current_player->bullets[i]->display();
        }
}

void engine::update(int ch)
{
    current_player->update(objects_position, ch);
    for(int i = 0 ; i < current_player->bullets.size(); i++)
        {
            current_player->bullets[i]->update(objects_position, ch);
        }
    auto& bullets = current_player->bullets;
    bullets.erase(std::remove_if(bullets.begin(), bullets.end(),
                                 [](bullet* b) { 
                                     if (!b->is_active) {
                                         delete b; 
                                         return true;
                                     }
                                     return false;
                                 }),
                  bullets.end());
}

void engine::run()
{
    start start_game;
    int ch;
    objects_position = start_game.map();
    // nodelay(stdscr, TRUE);
    curs_set(0);
    timeout(100); 

    while (true) 
    {
        ch = getch();
        if (ch == 'q')
            break;

        engine::update(ch);
        clear();
        
        start_game.map();
        engine::display();
        refresh();
    }
}
