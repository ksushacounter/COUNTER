package org.example.view;

import org.example.controller.PlayerController;
import org.example.model.GameObject;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;


public class GUIversion extends JPanel implements View {
    private List<GameObject> tires;
    private List<GameObject> prizes;
    GameObject player;
    private int roadY = 0;
    private Image playerSkin;
    private Image prizeSkin;
    private Image tireSkin;
    private int makeTireSkin = 0;
    private int makePrizeSkin = 0;


    public GUIversion(GameObject player, List<GameObject> tires, List<GameObject> prizes) throws IOException {
        this.player = player;
        this.tires = tires;
        this.prizes = prizes;
        InputStream inputStream = GUIversion.class.getResourceAsStream("/image/MegaPorshik.JPG");
        ImageIcon playerIcon = new ImageIcon(ImageIO.read(inputStream));
        playerSkin = playerIcon.getImage().getScaledInstance(player.getWidth(), player.getHeight(), Image.SCALE_SMOOTH);
        setFocusable(true);
    }

    @Override
    public void setRoadY(int roadY) {
        this.roadY = roadY;
    }

    @Override
    public String frameWork() {
        return "Swing";
    }

    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.setColor(Color.BLACK);
        g.fillRect(0, 0, getWidth(), getHeight());
        g.setColor(Color.WHITE);
        g.fillRect(190, roadY + 0, 10, 100);
        g.fillRect(190, roadY + 150, 10, 100);
        g.fillRect(190, roadY + 300, 10, 100);
        g.fillRect(190, roadY + 450, 10, 100);

        g.drawImage(playerSkin, player.getX(), player.getY(), this);
        if (!prizes.isEmpty() && makePrizeSkin == 0) {
            InputStream inputStream = GUIversion.class.getResourceAsStream("/image/kuboc.jpg");
            ImageIcon prizeIcon = null;
            try {
                prizeIcon = new ImageIcon(ImageIO.read(inputStream));
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            prizeSkin = prizeIcon.getImage().getScaledInstance(prizes.getFirst().getWidth(), prizes.getFirst().getHeight(), Image.SCALE_SMOOTH);
            makePrizeSkin = 1;
        }
        if (!tires.isEmpty() && makeTireSkin == 0) {
            InputStream inputStream = GUIversion.class.getResourceAsStream("/image/tire.jpg");
            ImageIcon tireIcon = null;
            try {
                tireIcon = new ImageIcon(ImageIO.read(inputStream));
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            tireSkin = tireIcon.getImage().getScaledInstance(tires.getFirst().getWidth(), tires.getFirst().getHeight(), Image.SCALE_SMOOTH);
            makeTireSkin = 1;
        }

        for (GameObject tire : tires) {
            g.drawImage(tireSkin, tire.getX(), tire.getY(), this);
        }
        for (GameObject prize : prizes) {
            g.drawImage(prizeSkin, prize.getX(), prize.getY(), this);
        }

        g.setColor(Color.RED);
        g.setFont(new Font("Arial", Font.BOLD, 24));
        g.drawString(player.getLives() + "lives", 300, 30);

        g.setColor(Color.PINK);
        g.setFont(new Font("Arial", Font.BOLD, 24));
        g.drawString(player.getPoints() + "points", 10, 30);
    }

    @Override
    public void KeyListener(PlayerController playerController) {
        this.addKeyListener(playerController);
    }

    @Override
    public void render() {
        this.repaint();
    }
}
