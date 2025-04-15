package org.example.model;

import org.example.view.GameOverView;
import org.example.view.Rendering;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Iterator;
import java.util.List;
import java.util.Random;

public class TimeAction implements ActionListener {
    int roadY = 0;
    int speed = 30;
    private Timer roadTimer;
    private Timer moveTireTimer;
    private Timer newTireTimer;
    private Rendering view;
    private List<GameObject> tires;
    private int tireX = 20;
    public GameObject player;

    public TimeAction(Rendering view, List<GameObject> tires, GameObject player){
        this.view = view;
        this.tires = tires;
        this.player = player;
        roadTimer = new Timer(16, this);
        moveTireTimer = new Timer(50, this);
        newTireTimer = new Timer(1000, this);
        roadTimer.start();
        moveTireTimer.start();
        newTireTimer.start();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if(e.getSource() == roadTimer) {
            roadY += speed;
            if (roadY >= 100) {
                roadY = 0;
            }
        }
        if(e.getSource() == moveTireTimer){
            Iterator<GameObject> iterator = tires.iterator();
            while(iterator.hasNext()){
                GameObject tire = iterator.next();
                if(!(Collision.checkCollision(player, tire))){
                    tire.moveDown();
                }else{
                    player.minusLives();
                    iterator.remove();
                    if(player.getLives() == 0){
                        GameOverView.show();
                    }
                }
            }
            view.changeTires(tires);
        }
        if(e.getSource() == newTireTimer){
            Random random = new Random();
            tireX = 20 + random.nextInt(340);
            tires.add(new Tire(tireX, 0));
            view.changeTires(tires);
        }
        view.setRoadY(roadY);
        view.repaint();
    }
}
