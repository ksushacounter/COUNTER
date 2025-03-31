package org.example.model;

import org.example.controller.PlayerController;
import org.example.view.Rendering;

import javax.swing.*;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        JFrame frame = new JFrame("007");
        frame.setSize(400, 675);

        Player player = new Player();
        List<Tire> tires = new ArrayList<Tire>();

        Rendering rendering = new Rendering(player, tires);
        PlayerController playerController = new PlayerController(player, rendering);

        frame.add(rendering);
        rendering.addKeyListener(playerController);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}
