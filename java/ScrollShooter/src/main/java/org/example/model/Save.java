package org.example.model;

import java.io.*;
import java.nio.file.Path;

public class Save {
    public static void save(GameObject player, String savePath) throws IOException {
        SavedGame savedGame = new SavedGame(player.getLives(), player.getPoints());
        try (FileOutputStream fileOutputStream = new FileOutputStream(savePath);
             ObjectOutputStream objectOutputStream = new ObjectOutputStream(fileOutputStream)) {
            objectOutputStream.writeObject(savedGame);
        }
    }

    public static SavedGame since(String savePath) throws IOException, ClassNotFoundException {
        try (FileInputStream inputStream = new FileInputStream(String.valueOf(savePath));
             ObjectInputStream objectInputStream = new ObjectInputStream(inputStream)) {
            return (SavedGame) objectInputStream.readObject();
        }
    }
}
