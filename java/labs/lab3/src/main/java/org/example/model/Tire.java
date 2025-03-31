package org.example.model;


public class Tire extends GameObject{
    private int x;
    private int y;

    public Tire(int x, int y){
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
        y -= 10;
    }
}
