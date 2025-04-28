package org.example.model;

import javax.swing.*;
import java.awt.*;

public class Prize extends GameObject{
    private int x;
    private int y;
    private int width = 40;
    private static int height = 60;

    public Prize(int x, int y){
        this.x = x;
        this.y = y;
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
    public int getWidth() {
        return width;
    }
    public int getHeight() {
        return height;
    }
}
