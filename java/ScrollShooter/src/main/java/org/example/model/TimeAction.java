package org.example.model;

import org.example.view.GameOverView;
import org.example.view.Rendering;

import javax.sound.sampled.*;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.IOException;
import java.util.Iterator;
import java.util.List;
import java.util.Random;

public class TimeAction implements ActionListener {
    int roadY = 0;
    int speed = 30;
    private Timer roadTimer;
    private Timer moveTireTimer;
    private Timer newTireTimer;
    private int moveTime = 50;
    private int newTime = 1000;
    private Rendering view;
    private List<GameObject> tires;
    private int tireX = 20;
    private GameObject player;
    private Clip clip;
    private File family = new File("C:/Users/garku/IdeaProjects/lab3/dominik-toretto-semya-jeto-glavnoe.wav");
    private File tokioDrift = new File("C:/Users/garku/IdeaProjects/lab3/Teriyaki_Boyz_-_Tokyo_Drift_Fast_Furious.wav");
    private AudioInputStream audio;


    public TimeAction(Rendering view, List<GameObject> tires, GameObject player) throws UnsupportedAudioFileException, LineUnavailableException, IOException {
        this.view = view;
        this.tires = tires;
        this.player = player;
        roadTimer = new Timer(16, this);
        moveTireTimer = new Timer(moveTime, this);
        newTireTimer = new Timer(newTime, this);
        start();
    }

    public void start() throws UnsupportedAudioFileException, IOException, LineUnavailableException {
        moveTireTimer = new Timer(moveTime, this);
        newTireTimer = new Timer(newTime, this);
        roadTimer.start();
        moveTireTimer.start();
        newTireTimer.start();
        if(clip != null) {
            clip.stop();
        }
        audio = AudioSystem.getAudioInputStream(tokioDrift);
        clip = AudioSystem.getClip();
        clip.open(audio);
        clip.start();
    }

    public void moreSpeed(){
        moveTime = moveTime - 25;
        newTime = newTime - 250;
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == roadTimer) {
            roadY += speed;
            if (roadY >= 100) {
                roadY = 0;
            }
        }
        if (e.getSource() == moveTireTimer) {
            Iterator<GameObject> iterator = tires.iterator();
            while (iterator.hasNext()) {
                GameObject tire = iterator.next();
                if (!(Collision.checkCollision(player, tire))) {
                    tire.moveDown();
                } else {
                    player.minusLives();
                    iterator.remove();
                    if (player.getLives() == 0) {
                        System.out.println("hhh");
                        try {
                            clip.stop();
                            audio = AudioSystem.getAudioInputStream(family);
                        } catch (UnsupportedAudioFileException ex) {
                            throw new RuntimeException(ex);
                        } catch (IOException ex) {
                            throw new RuntimeException(ex);
                        }
                        try {
                            clip = AudioSystem.getClip();
                        } catch (LineUnavailableException ex) {
                            throw new RuntimeException(ex);
                        }
                        try {
                            clip.open(audio);
                        } catch (LineUnavailableException ex) {
                            throw new RuntimeException(ex);
                        } catch (IOException ex) {
                            throw new RuntimeException(ex);
                        }
                        clip.start();
                        GameOverView.show();
                    }
                }
            }
            view.changeTires(tires);
        }
        if (e.getSource() == newTireTimer) {
            Random random = new Random();
            tireX = 20 + random.nextInt(340);
            tires.add(new Tire(tireX, 0));
            view.changeTires(tires);
        }
        view.setRoadY(roadY);
        view.repaint();
    }
}
