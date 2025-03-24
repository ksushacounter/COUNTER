package org.example.model;

public abstract class GameObject {
    int x;
    int y;

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
}
