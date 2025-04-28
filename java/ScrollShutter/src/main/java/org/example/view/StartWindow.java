package org.example.view;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;

public class StartWindow {
    private int difficulty;
    private int version;
    private boolean save = false;
    private boolean shouldClose = false;
    private boolean shouldCloseSave = false;

    public int getDifficulty() {
        return difficulty;
    }

    public int getVersion() {
        return version;
    }

    public boolean isSave() {
        return save;
    }

    public int start(String savePath) {
        JFrame frame = new JFrame();
        frame.setSize(400, 290);

        JPanel panel = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                InputStream inputStream = StartWindow.class.getResourceAsStream("/image/start.jpg");
                ImageIcon bgImage = null;
                try {
                    bgImage = new ImageIcon(ImageIO.read(inputStream));
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
                g.drawImage(bgImage.getImage(), 0, 0, getWidth(), getHeight(), null);
            }
        };
        panel.setLayout(new FlowLayout());

        JButton hard = new JButton("hard");
        JButton medium = new JButton("medium");
        JButton simple = new JButton("simple");
        JButton GUI = new JButton("graphic");
        JButton TUI = new JButton("terminal");

        hard.setBackground(Color.RED);
        hard.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                difficulty = 1;
                hard.setBackground(Color.gray);
                simple.setBackground(Color.GREEN);
                medium.setBackground(Color.YELLOW);
            }
        });

        medium.setBackground(Color.YELLOW);
        medium.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                difficulty = 2;
                medium.setBackground(Color.gray);
                simple.setBackground(Color.GREEN);
                hard.setBackground(Color.RED);
            }
        });

        simple.setBackground(Color.GREEN);
        simple.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                difficulty = 3;
                simple.setBackground(Color.gray);
                hard.setBackground(Color.RED);
                medium.setBackground(Color.YELLOW);
            }
        });

        GUI.setBackground(Color.MAGENTA);
        GUI.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                version = 1;
                GUI.setBackground(Color.gray);
                TUI.setBackground(Color.MAGENTA);
            }
        });


        TUI.setBackground(Color.MAGENTA);
        TUI.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                version = 2;
                TUI.setBackground(Color.gray);
                GUI.setBackground(Color.MAGENTA);
            }
        });

        JButton start = new JButton("start");
        start.setBackground(Color.WHITE);
        start.addActionListener(e -> {
            if (difficulty == 0 || version == 0) {
                JOptionPane.showMessageDialog(frame, "Choose the difficulty and version!");
                return;
            } else {
                File file = new File(savePath);
                if (file.exists()) {
                    Object[] options = {"Yes", "No"};
                    int choice = JOptionPane.showOptionDialog(frame,
                            "You have a save! Should I start with it?",
                            "Save Found",
                            JOptionPane.YES_NO_OPTION,
                            JOptionPane.QUESTION_MESSAGE,
                            null,
                            options,
                            options[0]);

                    save = (choice == JOptionPane.YES_OPTION);
                }
                shouldClose = true;
                frame.dispose();

            }
        });

        panel.add(hard);
        panel.add(medium);
        panel.add(simple);
        panel.add(GUI);
        panel.add(TUI);
        panel.add(start);

        frame.add(panel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);

        while (!shouldClose) {
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        return 0;
    }
}