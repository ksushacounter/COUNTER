package org.example.model;


import javax.swing.*;
import java.awt.*;

public class Tire extends GameObject{
    private int x;
    private int y;
    private Image skin;
    private int width = 40;
    private int height = 70;

    public Tire(int x, int y){
        this.x = x;
        this.y = y;
        ImageIcon tire = new ImageIcon("C:/Users/garku/IdeaProjects/lab3/tire.jpg");
        skin = tire.getImage().getScaledInstance(width, height, Image.SCALE_SMOOTH);
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public void moveDown(){
        this.y += 10;
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
