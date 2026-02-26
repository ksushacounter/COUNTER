package org.example.model;


import org.example.view.GameOverView;

import javax.swing.*;
import java.awt.*;
import java.io.IOException;

public class Tire extends GameObject {
    private int x;
    private int y;
    private int width = 40;
    private int height = 70;

    public Tire(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

    public boolean moveDown(int version, ObjectsState objectsState) {
        boolean collision = false;
        if (version == 2) {
            collision = Collision.lanternaCheckCollision(objectsState.getPlayer(), this);
        } else {
            collision = Collision.checkCollision(objectsState.getPlayer(), this);
        }
        if (!collision) {
            this.y += 10;
            return true;
        } else {
            objectsState.getPlayer().minusLives();
            if (objectsState.getPlayer().getLives() == 0) {
                try {
                    objectsState.gameOver();
                } catch (IOException ex) {
                    throw new RuntimeException(ex);
                }
            }
            return false;
        }
    }
}

