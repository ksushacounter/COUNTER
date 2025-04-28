package org.example.controller;

import com.googlecode.lanterna.input.KeyStroke;
import com.googlecode.lanterna.input.KeyType;
import org.example.model.GameObject;
import org.example.model.Save;
import org.example.view.View;

import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.io.IOException;


public class PlayerController extends KeyAdapter {
    private GameObject player;
    private View view;
    private String savePath;

    public PlayerController(GameObject player, View view, String savePath) {
        this.player = player;
        this.view = view;
        this.savePath = savePath;
    }

    @Override
    public void keyPressed(KeyEvent e) {
        int key = e.getKeyCode();

        if (key == KeyEvent.VK_LEFT) {
            player.moveLeft();
        } else if (key == KeyEvent.VK_RIGHT) {
            player.moveRight();
        }

        try {
            view.render();
        } catch (IOException ex) {
            throw new RuntimeException(ex);
        }
    }

    public void keyPressedLanterna(KeyStroke keyStroke) throws IOException {
        if (keyStroke == null) return;

        switch (keyStroke.getKeyType()) {
            case ArrowLeft -> player.moveLeft();
            case ArrowRight -> player.moveRight();
            case F2 -> Save.save(player, savePath);
        }
        try {
            view.render();
//            System.out.println(player.getX() + ' ' + player.getY());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}

