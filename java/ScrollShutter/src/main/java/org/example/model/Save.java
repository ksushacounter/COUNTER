package org.example.model;

import java.io.*;

public class Save {
    public static void save(GameObject player, String savePath) throws IOException {
        SavedGame savedGame = new SavedGame(player.getLives(), player.getPoints());

        FileOutputStream fileOutputStream = new FileOutputStream(savePath);
        ObjectOutputStream objectOutputStream = new ObjectOutputStream(fileOutputStream);
        objectOutputStream.writeObject(savedGame);

        objectOutputStream.close();
    }

    public static SavedGame since(String savePath) throws IOException, ClassNotFoundException {
        FileInputStream fileInputStream = new FileInputStream(savePath);
        ObjectInputStream objectInputStream = new ObjectInputStream(fileInputStream);
        SavedGame savedGame = (SavedGame) objectInputStream.readObject();

        return savedGame;
    }
}
