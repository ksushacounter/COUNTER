package org.example;

import org.example.controller.PlayerController;
import org.example.model.*;
import org.example.view.*;
import javafx.application.Platform;


import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;
import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.IOException;
//:)

public class Main {
    private static Player player;
    private static ObjectsState objectsState;
    private static View rendering;
    private static TimeAction timeAction;
    private static PlayerController playerController;
    private static int difficulty = 1;
    private static int version;
    private static final String savePath = System.getProperty("user.dir") + File.separator + "save.ser";
    public static void initialiseGUIGame() throws UnsupportedAudioFileException, IOException, LineUnavailableException {
        Platform.startup(() -> {
        });
        JFrame frame = new JFrame("Fast&Furious");
        frame.setSize(400, 675);

        rendering = new GUIversion(objectsState);
        GameOverView gameOverView = new GameOverView(objectsState);
        timeAction = new TimeAction(objectsState, difficulty, version);
        playerController = new PlayerController(player, rendering, savePath);
        frame.add((Component) rendering);
        JButton save = new JButton("save");
        save.addActionListener(e -> {
            try {
                Save.save(player, savePath);
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        });
        frame.add(save, BorderLayout.NORTH);
        rendering.KeyListener(playerController);
        objectsState.addListener((Listener) rendering);
        objectsState.addListener(gameOverView);
        frame.setVisible(true);
        ((Component) rendering).requestFocusInWindow();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public static void initialiseTUIGame() throws IOException, UnsupportedAudioFileException, LineUnavailableException {
        rendering = new TUIversion(objectsState);
        timeAction = new TimeAction(objectsState, difficulty, version);
        playerController = new PlayerController(player, rendering, savePath);
        rendering.KeyListener(playerController);
    }

    public static void restartGame() throws UnsupportedAudioFileException, LineUnavailableException, IOException {
        player.newLives();
        player.newPoints();
        objectsState = new ObjectsState(player);
        timeAction.start();
    }


    public static void main(String[] args) throws UnsupportedAudioFileException, LineUnavailableException, IOException, ClassNotFoundException {
        StartWindow start = new StartWindow();
        start.start(savePath);
        difficulty = start.getDifficulty();
        version = start.getVersion();
        boolean startWithSave = start.isSave();
        if(startWithSave) {
            SavedGame savedGame = Save.since(savePath);
            player = new Player(savedGame.getLives(), savedGame.getPoints());
        }
        else{
            player = new Player();
        }
        objectsState = new ObjectsState(player);

        switch (version){
            case 1:
                initialiseGUIGame();
                break;
            case 2:
                initialiseTUIGame();
                break;
        }
    }

}
//
//package org.example.model;
//
//import org.example.controller.PlayerController;
//import org.example.view.TUIversion;
//import com.googlecode.lanterna.terminal.Terminal;
//import org.example.view.View;
//
//import java.io.IOException;
//import java.util.ArrayList;
//import java.util.List;
//
//public class Main {
//    private static Terminal terminal;
//    private static Player player;
//    private static List<GameObject> tires;
//    private static List<GameObject> prizes;
//    private static View rendering;
//    private static TimeAction timeAction;
//    private static PlayerController playerController;
//    private static int difficulty = 1;
//
//    public static void initialiseGame() throws Exception {
//        rendering = new TUIversion(player, tires, prizes);
//        timeAction = new TimeAction(rendering, tires, prizes, player, difficulty);
//        playerController = new PlayerController(player, rendering);
//        rendering.KeyListener(playerController);
//    }
//
//    public static void restartGame() throws Exception {
//        player.newLives();
//        player.newPoints();
//        tires.clear();
//        prizes.clear();
//        timeAction.start();
//    }
//
//    public static void main(String[] args) {
//        try {
//            player = new Player();
//            tires = new ArrayList<>();
//            prizes = new ArrayList<>();
//            initialiseGame();
//            timeAction.start();
//
//        } catch (Exception e) {
//            e.printStackTrace();
//        } finally {
//            try {
//                if (terminal != null) {
//                    terminal.close();
//                }
//            } catch (IOException e) {
//                e.printStackTrace();
//            }
//        }
//    }
//
//}
