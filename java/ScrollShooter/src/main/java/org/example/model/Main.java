package org.example.model;

import org.example.controller.PlayerController;
import org.example.view.Rendering;
import javafx.application.Platform;


import javax.swing.*;
import java.util.ArrayList;
import java.util.List;

public class Main {
    private static JFrame frame;
    private static Player player;
    private static List<GameObject> tires;
    private static Rendering rendering;
    private static TimeAction timeAction;
    private static PlayerController playerController;

    public static void initialiseGame(){
        Platform.startup(() -> {});
        rendering = new Rendering(player, tires);
        timeAction = new TimeAction(rendering, tires, player);
        playerController = new PlayerController(player, rendering);

        frame.add(rendering);
        rendering.addKeyListener(playerController);
        frame.setVisible(true);
    }
    public static void main(String[] args) {
        frame = new JFrame("007");
        frame.setSize(400, 675);
        player = new Player();
        tires = new ArrayList<GameObject>();
        initialiseGame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public static void restartGame() {
        tires.clear();
        player.newLives();
        System.out.println(timeAction.player.getLives());

        initialiseGame();
    }

}
