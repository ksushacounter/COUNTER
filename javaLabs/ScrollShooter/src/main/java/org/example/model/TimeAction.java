package org.example.model;

import java.io.IOException;
import java.util.Iterator;
import java.util.Objects;
import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;

public class TimeAction {
    private final int difficulty;
    private final Timer gameTimer;
    private final ObjectsState objectsState;
    private GameObject collisionTire;
    private int countTire = 0;
    private final int version;

    public TimeAction(ObjectsState objectsState, int difficulty, int version) {
        this.objectsState = objectsState;
        this.difficulty = difficulty;
        this.version = version;
        this.gameTimer = new Timer(true);
        start();
    }

    public void start() {
        gameTimer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                updateRoad();
            }
        }, 0, 16);

        gameTimer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                moveObjects();
            }
        }, 0, 20 * difficulty);

        gameTimer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                spawnNewTire();
            }
        }, 0, 400 * difficulty);

        gameTimer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                spawnNewPrize();
            }
        }, 0, 1205 * difficulty);
    }

    public void stop() {
        gameTimer.cancel();
    }

    private void updateRoad() {
        try {
            int speed = 30;
            objectsState.setRoadY(speed);
            if (objectsState.getRoadY() >= 100) {
                objectsState.zeroRoadY();
            }

        } catch (IOException ex) {
            throw new RuntimeException("Road update failed", ex);
        }
    }

    private void moveObjects() {
        Iterator<GameObject> tireIterator = objectsState.getTires().iterator();
        Iterator<GameObject> prizeIterator = objectsState.getPrizes().iterator();

        while (tireIterator.hasNext()) {
            GameObject tire = tireIterator.next();
            if (!tire.moveDown(version, objectsState)) {
                tireIterator.remove();
            }
        }

        while (prizeIterator.hasNext()) {
            GameObject prize = prizeIterator.next();
            if (!prize.moveDown(version, objectsState)) {
                prizeIterator.remove();
            }
        }
    }

    private void spawnNewTire() {
        Random random = new Random();
        int tireX = 20 + random.nextInt(340);
        try {
            objectsState.addTires(new Tire(tireX, 0));
            countTire++;
            if (countTire == 3) {
                collisionTire = objectsState.getTires().getLast();
                countTire = 0;
            }
        } catch (IOException ex) {
            throw new RuntimeException("Failed to spawn tire", ex);
        }
    }

    private void spawnNewPrize() {
        boolean collision = false;
        GameObject newPrize;
        do {
            Random random = new Random();
            newPrize = new Prize(20 + random.nextInt(340), 0);
            if(collisionTire != null) {
                if (version == 2) {
                    collision = Collision.lanternaCheckCollision(collisionTire, newPrize);
                } else {
                    collision = Collision.checkCollision(collisionTire, newPrize);
                }
            }
        } while (collision);

        try {
            objectsState.addPrizes(newPrize);
        } catch (IOException ex) {
            throw new RuntimeException("Failed to spawn prize", ex);
        }
    }
}
