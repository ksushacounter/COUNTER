package org.example.model;

import javax.swing.*;
import java.awt.*;

public class Player extends GameObject {
    private int x = 160;
    private int y = 440;
    private int lives = 5;
    private int points = 0;
    private int width = 50;
    private int height = 115;

    public Player() {
    }

    public Player(int lives, int points) {
        this.lives = lives;
        this.points = points;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public void moveLeft() {
        x -= 10;
    }

    public void moveRight() {
        x += 10;
    }

    @Override
    public int getLives() {
        return lives;
    }

    @Override
    public void minusLives() {
        this.lives = lives - 1;
    }

    public void newLives() {
        this.lives = 5;
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

    public int getPoints() {
        return points;
    }
    public void addPoints() {
        points = points + 1;
    }

    @Override
    public boolean moveDown(int version, ObjectsState objectsState) {
        return true;
    }

    public void newPoints(){
        points = 0;
    }
}
