package org.example;

import org.example.controller.PlayerController;
import org.example.model.Player;
import org.example.model.Tire;
import org.example.view.Rendering;

import javax.swing.*;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        JFrame frame = new JFrame("007");
        frame.setSize(400, 675);

        Player player = new Player();
//        List<Tire> tires;
//        for(int i = )
        Rendering rendering = new Rendering(player);
        PlayerController playerController = new PlayerController(player, rendering);

        frame.add(rendering);
        rendering.addKeyListener(playerController);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}
