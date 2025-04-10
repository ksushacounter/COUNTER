package org.example.model;

import java.awt.*;
import java.lang.ref.PhantomReference;
import java.util.PrimitiveIterator;

public abstract class GameObject {
    private int x;
    private int y;
    private int lives;
    private Image skin;
    private int width;
    private int height;

    public int getX(){
        return x;
    }
    public int getY(){
        return y;
    }
    public void moveLeft() {
        x -= 10;
    }

    public void moveRight() {
        x += 10;
    }

    public void moveDown(){
        y -= 10;
    }

    public int getLives() {
        return lives;
    }
    public void minusLives() {
        this.lives = lives - 1;
    }
    public void newLives() {
        this.lives = 5;
    }

    public Image getSkin() {
        return skin;
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }
}
