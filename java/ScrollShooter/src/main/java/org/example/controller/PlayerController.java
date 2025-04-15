package org.example.controller;

import org.example.model.GameObject;
import org.example.view.Rendering;

import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class PlayerController extends KeyAdapter {
    private GameObject player;
    private Rendering view;

    public PlayerController(GameObject player, Rendering view) {
        this.player = player;
        this.view = view;
    }

    @Override
    public void keyPressed(KeyEvent e) {
        int key = e.getKeyCode();

        if (key == KeyEvent.VK_LEFT) {
            player.moveLeft();
        } else if (key == KeyEvent.VK_RIGHT) {
            player.moveRight();
        }

        view.repaint();
    }
}
