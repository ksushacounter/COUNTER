package org.example.model;

public class Player extends GameObject {
    private int x = 160;
    private int y = 440;

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
}
