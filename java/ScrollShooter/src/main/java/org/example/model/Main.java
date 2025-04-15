package org.example.model;

import org.example.controller.PlayerController;
import org.example.view.Rendering;
import javafx.application.Platform;


import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;
import javax.swing.*;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main {
    private static JFrame frame;
    private static Player player;
    private static List<GameObject> tires;
//    private static List<GameObject> tires;
    private static Rendering rendering;
    private static TimeAction timeAction;
    private static PlayerController playerController;

    public static void initialiseGame() throws UnsupportedAudioFileException, IOException, LineUnavailableException {
        Platform.startup(() -> {});
        rendering = new Rendering(player, tires);
        timeAction = new TimeAction(rendering, tires, player);
        playerController = new PlayerController(player, rendering);
        frame.add(rendering);
        rendering.addKeyListener(playerController);
        frame.setVisible(true);
    }

    public static void restartGame() throws UnsupportedAudioFileException, LineUnavailableException, IOException {
        player.newLives();
        tires.clear();
        timeAction.moreSpeed();
        timeAction.start();
    }


    public static void main(String[] args) throws UnsupportedAudioFileException, LineUnavailableException, IOException {
        frame = new JFrame("007");
        frame.setSize(400, 675);
        player = new Player();
        tires = new ArrayList<GameObject>();
        initialiseGame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

}
