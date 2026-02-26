package org.example.model;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.util.Iterator;
import java.util.Objects;
import java.util.Random;

public class TimeActionNotUsed implements ActionListener {
    private final int difficulty;
    private final Timer roadTimer;
    private Timer moveObjectsTimer;
    private Timer newTireTimer;
    private Timer newPrizeTimer;
    private final ObjectsState objectsState;
    private GameObject collisionTire;
    private int countTire = 0;
    private final int version;


    public TimeActionNotUsed(ObjectsState objectsState, int difficulty, int version) throws IOException {
        this.objectsState = objectsState;
        this.difficulty = difficulty;
        this.version = version;
        roadTimer = new Timer(16, this);
        start();
    }

    public void start() throws IOException {
        int moveTime = 20;
        moveObjectsTimer = new Timer(moveTime * difficulty, this);
        int newTime = 400;
        newTireTimer = new Timer(newTime * difficulty, this);
        int newPrizeTime = 1205;
        newPrizeTimer = new Timer(newPrizeTime * difficulty, this);
        roadTimer.start();
        moveObjectsTimer.start();
        newTireTimer.start();
        newPrizeTimer.start();

    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == roadTimer) {
            try {
                int speed = 30;
                objectsState.setRoadY(speed);
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
            ;
            if (objectsState.getRoadY() >= 100) {
                try {
                    objectsState.zeroRoadY();
                } catch (IOException ex) {
                    throw new RuntimeException(ex);
                }
            }
        }
        if (e.getSource() == moveObjectsTimer) {
            Iterator<GameObject> tireIterator = objectsState.getTires().iterator();
            Iterator<GameObject> prizeIterator = objectsState.getPrizes().iterator();
            while (tireIterator.hasNext()) {
                GameObject tire = tireIterator.next();
                if(Objects.equals(tire.moveDown(version, objectsState), "boom")) {
                    tireIterator.remove();
                }
            }
            while (prizeIterator.hasNext()) {
                GameObject prize = prizeIterator.next();
                if(Objects.equals(prize.moveDown(version, objectsState), "boom")){
                    prizeIterator.remove();

                }
            }

        }

        if (e.getSource() == newTireTimer) {
            Random random = new Random();
            int tireX = 20 + random.nextInt(340);
            try {
                objectsState.addTires(new Tire(tireX, 0));
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
            countTire = countTire + 1;
            if (countTire == 3) {
                collisionTire = objectsState.getTires().getLast();
                countTire = 0;
            }
        }
        if (e.getSource() == newPrizeTimer) {
            boolean collision = false;
            GameObject newPrize;
            do {
                Random random = new Random();
                newPrize = new Prize(20 + random.nextInt(340), 0);
                if (version == 2) {
                    collision = Collision.lanternaCheckCollision(collisionTire, newPrize);
                } else {
                    collision = Collision.checkCollision(collisionTire, newPrize);
                }
            }
            while (collision);
            try {
                objectsState.addPrizes(newPrize);
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        }
        try {
            int roadY = 0;
            objectsState.setRoadY(roadY);
        } catch (IOException ex) {
            throw new RuntimeException(ex);
        }
    }
}

