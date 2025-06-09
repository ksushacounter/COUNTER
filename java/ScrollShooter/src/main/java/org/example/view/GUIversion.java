package org.example.view;

import org.example.controller.PlayerController;
import org.example.model.GameObject;
import org.example.model.Listener;
import org.example.model.ObjectsState;

import javax.imageio.ImageIO;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;
import javax.swing.*;
import java.awt.*;
import java.io.IOException;
import java.io.InputStream;


public class GUIversion extends JPanel implements View, Listener {
    private Image playerSkin;
    private Image prizeSkin;
    private Image tireSkin;
    private int makeTireSkin = 0;
    private int makePrizeSkin = 0;
    private ObjectsState objectsState;
    private Audio audio;


    public GUIversion(ObjectsState objectsState) throws IOException, UnsupportedAudioFileException, LineUnavailableException {
        this.objectsState = objectsState;
        try (InputStream inputStream = GUIversion.class.getResourceAsStream("/image/MegaPorshik.JPG")) {
            if (audio != null) {
                audio.stopAndClose();
            }
            this.audio = new Audio();
            assert inputStream != null;
            ImageIcon playerIcon = new ImageIcon(ImageIO.read(inputStream));
            playerSkin = playerIcon.getImage().getScaledInstance(objectsState.getPlayer().getWidth(), objectsState.getPlayer().getHeight(), Image.SCALE_SMOOTH);
        }
        setFocusable(true);
    }

    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.setColor(Color.BLACK);
        g.fillRect(0, 0, getWidth(), getHeight());
        g.setColor(Color.WHITE);
        g.fillRect(190, objectsState.getRoadY(), 10, 100);
        g.fillRect(190, objectsState.getRoadY() + 150, 10, 100);
        g.fillRect(190, objectsState.getRoadY() + 300, 10, 100);
        g.fillRect(190, objectsState.getRoadY() + 450, 10, 100);

        g.drawImage(playerSkin, objectsState.getPlayer().getX(), objectsState.getPlayer().getY(), this);
        if (!objectsState.getPrizes().isEmpty() && makePrizeSkin == 0) {
            try (InputStream inputStream = GUIversion.class.getResourceAsStream("/image/kuboc.jpg")) {
                ImageIcon prizeIcon = null;
                prizeIcon = new ImageIcon(ImageIO.read(inputStream));

                prizeSkin = prizeIcon.getImage().getScaledInstance(objectsState.getPrizes().getFirst().getWidth(), objectsState.getPrizes().getFirst().getHeight(), Image.SCALE_SMOOTH);
                makePrizeSkin = 1;
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        if (!objectsState.getTires().isEmpty() && makeTireSkin == 0) {
            try(InputStream inputStream = GUIversion.class.getResourceAsStream("/image/tire.jpg")) {
                ImageIcon tireIcon = null;
                tireIcon = new ImageIcon(ImageIO.read(inputStream));
                tireSkin = tireIcon.getImage().getScaledInstance(objectsState.getTires().getFirst().getWidth(), objectsState.getTires().getFirst().getHeight(), Image.SCALE_SMOOTH);
                makeTireSkin = 1;
            }
            catch (IOException e) {
                throw new RuntimeException(e);
            }
        }

        for (GameObject tire : objectsState.getTires()) {
            g.drawImage(tireSkin, tire.getX(), tire.getY(), this);
        }
        for (GameObject prize : objectsState.getPrizes()) {
            g.drawImage(prizeSkin, prize.getX(), prize.getY(), this);
        }

        g.setColor(Color.RED);
        g.setFont(new Font("Arial", Font.BOLD, 24));
        g.drawString(objectsState.getPlayer().getLives() + "lives", 300, 30);

        g.setColor(Color.PINK);
        g.setFont(new Font("Arial", Font.BOLD, 24));
        g.drawString(objectsState.getPlayer().getPoints() + "points", 10, 30);
    }

    @Override
    public void KeyListener(PlayerController playerController) {
        this.addKeyListener(playerController);
    }

    @Override
    public void render() {
        this.repaint();
    }

    @Override
    public void modelChanged() {
        if (objectsState.isGameOver()) {
            audio.GameOver();
        }
        this.repaint();
    }
}
