package org.example.model;

import javax.swing.*;
import java.awt.*;

public class Player extends GameObject {
    private int x = 160;
    private int y = 440;
    private int lives = 5;
    private Image skin;
    private int width = 50;
    private int height = 115;

    public Player(){
        ImageIcon icon = new ImageIcon("C:/Users/garku/IdeaProjects/lab3/MegaPorshik.JPG");
        skin = icon.getImage().getScaledInstance(width, height, Image.SCALE_SMOOTH);
    }
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
