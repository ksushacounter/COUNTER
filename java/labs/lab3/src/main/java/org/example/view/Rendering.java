package org.example.view;

import org.example.model.GameObject;
import org.example.model.Tire;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;


public class Rendering extends JPanel  {
    private List<GameObject> tires;
    GameObject player;
    private int roadY = 0;

    public Rendering(GameObject player, List<GameObject> tires) {
        this.player = player;
        this.tires = tires;
        setFocusable(true);
    }

    public void setRoadY(int roadY){
        this.roadY = roadY;
    }
    public void changeTires(List<GameObject> tires){
        this.tires = tires;
    }

    public void paintComponent(Graphics g){
        super.paintComponent(g);
        g.setColor(Color.BLACK);
        g.fillRect(0, 0, getWidth(), getHeight());
        g.setColor(Color.WHITE);
        g.fillRect(190, roadY + 0, 10, 100);
        g.fillRect(190, roadY + 150, 10, 100);
        g.fillRect(190, roadY + 300, 10, 100);
        g.fillRect(190, roadY + 450, 10, 100);

        g.drawImage(player.getSkin(), player.getX(), player.getY(), this);
        for(GameObject tire : tires){
            g.drawImage(tire.getSkin(), tire.getX(), tire.getY(), this);
        }

        g.setColor(Color.RED);
        g.setFont(new Font("Arial", Font.BOLD, 24));
        g.drawString(player.getLives() + "lives", 300, 30);
    }
}
