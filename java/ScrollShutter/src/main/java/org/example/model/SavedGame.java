package org.example.model;

import java.io.Serializable;

public class SavedGame implements Serializable {
    private int lives;
    private int points;

    public SavedGame(int lives, int points){
        this.lives = lives;
        this.points = points;
    }

    public int getLives() {
        return lives;
    }

    public int getPoints() {
        return points;
    }
}
