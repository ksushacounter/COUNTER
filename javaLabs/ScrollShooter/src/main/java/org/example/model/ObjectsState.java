package org.example.model;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class ObjectsState {
    private List<GameObject> tires;
    private List<GameObject> prizes;
    private GameObject player;
    private List<Listener> listeners = new ArrayList<>();
    private int roadY = 0;
    private boolean gameOver = false;

    public ObjectsState(GameObject player){
        this.player = player;
        this.tires = new ArrayList<GameObject>();
        this.prizes = new ArrayList<GameObject>();
    }

    public void addTires(GameObject tire) throws IOException {
        this.tires.add(tire);
        notifyListeners();
    }

    public void addPrizes(GameObject prize) throws IOException {
        this.prizes.add(prize);
        notifyListeners();
    }


    public GameObject getPlayer() {
        return player;
    }

    public int getRoadY() {
        return roadY;
    }

    public List<GameObject> getTires(){
        return tires;
    }

    public List<GameObject> getPrizes(){
        return prizes;
    }

    public void setRoadY(int speed) throws IOException {
        this.roadY = roadY + speed;
        notifyListeners();
    }
    public void zeroRoadY() throws IOException {
        this.roadY = 0;
        notifyListeners();
    }

    public void gameOver() throws IOException {
        this.gameOver = true;
        notifyListeners();
    }

    public boolean isGameOver() {
        return gameOver;
    }

    public void removeListeners(Listener listener) {
        this.listeners.remove(listener);
    }

    public void addListener(Listener listener) {
        this.listeners.add(listener);
    }

    private void notifyListeners() throws IOException {
        for (Listener listener : listeners) {
            listener.modelChanged();
        }
        this.gameOver = false;
    }
}
