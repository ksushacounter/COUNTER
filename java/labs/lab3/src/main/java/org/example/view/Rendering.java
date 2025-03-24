package org.example.view;


import org.example.model.GameObject;

import javax.swing.*;
import java.awt.*;

public class Rendering extends JPanel {
    private Image skinPlayer;
    private Image skinTire;
    GameObject player;
    GameObject tire;

    public Rendering(GameObject player) {
        this.player = player;
        this.tire = tire;
        ImageIcon icon = new ImageIcon("C:/Users/garku/IdeaProjects/k.garkusha/java/labs/lab3/MegaPorshik.JPG");
        skinPlayer = icon.getImage().getScaledInstance(50, 115, Image.SCALE_SMOOTH);
        setFocusable(true);
    }

    public void paintComponent(Graphics g){
        super.paintComponent(g);
        g.setColor(Color.BLACK);
        g.fillRect(0, 0, getWidth(), getHeight());
        g.drawImage(skinPlayer, player.getX(), player.getY(), this);
    }
}
