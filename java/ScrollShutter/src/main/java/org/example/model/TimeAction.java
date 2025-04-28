package org.example.model;

import org.example.view.GameOverView;
import org.example.view.View;

import javax.sound.sampled.*;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.util.Iterator;
import java.util.List;
import java.util.Objects;
import java.util.Random;

public class TimeAction implements ActionListener {
    private int roadY = 0;
    private int speed = 30;
    private int difficulty;
    private Timer roadTimer;
    private Timer moveObjectsTimer;
    private Timer newTireTimer;
    private Timer newPrizeTimer;
    private int moveTime = 20;
    private int newTime = 400;
    private int newPrizeTime = 1205;
    private View view;
    private List<GameObject> tires;
    private List<GameObject> prizes;
    private int tireX = 20;
    private GameObject player;
    private Audio audio;
    private GameObject newPrize;
    private GameObject colissionTire;
    private int countTire = 0;
    private int maxPrizes = 10;


    public TimeAction(View view, List<GameObject> tires, List<GameObject> prizes, GameObject player, int difficulty) throws UnsupportedAudioFileException, LineUnavailableException, IOException {
        this.view = view;
        this.tires = tires;
        this.prizes = prizes;
        this.player = player;
        this.difficulty = difficulty;
        roadTimer = new Timer(16, this);
        start();
    }

    public void start() throws UnsupportedAudioFileException, LineUnavailableException, IOException {
        moveObjectsTimer = new Timer(moveTime * difficulty, this);
        newTireTimer = new Timer(newTime * difficulty, this);
        newPrizeTimer = new Timer(newPrizeTime * difficulty, this);
        if (audio != null) {
            audio.stopAndClose();
        }
        this.audio = new Audio();
        roadTimer.start();
        moveObjectsTimer.start();
        newTireTimer.start();
        newPrizeTimer.start();

    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == roadTimer) {
            roadY += speed;
            if (roadY >= 100) {
                roadY = 0;
            }
        }
        if (e.getSource() == moveObjectsTimer) {
            Iterator<GameObject> tireIterator = tires.iterator();
            Iterator<GameObject> prizeIterator = prizes.iterator();
            while (tireIterator.hasNext()) {
                boolean collision = false;
                GameObject tire = tireIterator.next();
                if (Objects.equals(view.frameWork(), "Lanterna")) {
                    collision = Collision.lanternaCheckCollision(player, tire);
                } else {
                    collision = Collision.checkCollision(player, tire);
                }
                if (!collision) {
                    tire.moveDown();
                } else {
                    player.minusLives();
                    tireIterator.remove();
                    if (player.getLives() == 0) {
                        audio.GameOver();
                        GameOverView.show(player.getPoints());
                    }
                }
            }
            while (prizeIterator.hasNext()) {
                GameObject prize = prizeIterator.next();
                boolean collision;
                if (Objects.equals(view.frameWork(), "Lanterna")) {
                    collision = Collision.lanternaCheckCollision(player, prize);
                } else {
                    collision = Collision.checkCollision(player, prize);
                }
                if (!collision) {
                    prize.moveDown();
                } else {
                    player.addPoints();
                    prizeIterator.remove();
                    if (player.getPoints() == maxPrizes) {
                        audio.GameOver();
                        GameOverView.show(player.getPoints());
                        roadTimer.stop();
                        moveObjectsTimer.stop();
                        newTireTimer.stop();
                        newPrizeTimer.stop();
                    }
                }
            }

        }

        if (e.getSource() == newTireTimer) {
            Random random = new Random();
            tireX = 20 + random.nextInt(340);
            tires.add(new Tire(tireX, 0));
            countTire = countTire + 1;
            if (countTire == 3) {
                colissionTire = tires.getLast();
                countTire = 0;
            }
        }
        if (e.getSource() == newPrizeTimer) {
            Random random = new Random();
            boolean collision = false;
            do {
                newPrize = new Prize(20 + random.nextInt(340), 0);
                if (Objects.equals(view.frameWork(), "Lanterna")) {
                    collision = Collision.lanternaCheckCollision(colissionTire, newPrize);
                } else {
                    collision = Collision.checkCollision(colissionTire, newPrize);
                }
            }
            while (collision);
            prizes.add(newPrize);
        }
        view.setRoadY(roadY);
        try {
            view.render();
        } catch (
                IOException ex) {
            throw new RuntimeException(ex);
        }
    }
}

