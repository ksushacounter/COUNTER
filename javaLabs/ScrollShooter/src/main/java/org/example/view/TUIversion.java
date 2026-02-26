package org.example.view;

import com.googlecode.lanterna.SGR;
import com.googlecode.lanterna.TerminalSize;
import com.googlecode.lanterna.TextColor;
import com.googlecode.lanterna.gui2.*;
import com.googlecode.lanterna.input.KeyStroke;
import com.googlecode.lanterna.screen.Screen;
import com.googlecode.lanterna.screen.TerminalScreen;
import com.googlecode.lanterna.terminal.swing.SwingTerminal;
import org.example.controller.PlayerController;
import org.example.model.GameObject;
import org.example.model.Listener;
import org.example.model.ObjectsState;

import javax.swing.*;
import java.io.IOException;

public class TUIversion implements View, Listener {
    private final ObjectsState objectsState;
    private final MultiWindowTextGUI gui;
    private final Panel gamePanel;
    private final BasicWindow window;
    private final int windowWidth = 500;
    private final int windowHeight = 400;
    private final int gridWidth = 30;
    private final int gridHeight = 20;

    public TUIversion(ObjectsState objectsState) throws IOException {
        this.objectsState = objectsState;

        SwingTerminal terminal = new SwingTerminal();
        JFrame frame = new JFrame("Lanterna TUI Game");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.getContentPane().add(terminal);
        frame.setSize(windowWidth, windowHeight);
        frame.setVisible(true);

        Screen screen = new TerminalScreen(terminal);
        screen.startScreen();

        gui = new MultiWindowTextGUI(screen, new DefaultWindowManager(), new EmptySpace(TextColor.ANSI.BLACK));

        gamePanel = new Panel(new GridLayout(gridWidth));

        window = new BasicWindow("TUI Game");
        window.setComponent(gamePanel);
        gui.addWindow(window);
    }

    @Override
    public void render() throws IOException {
        gamePanel.removeAllComponents();

        StringBuilder sb = new StringBuilder();
        for (int y = 0; y < gridHeight; y++) {
            for (int x = 0; x < gridWidth; x++) {
                boolean drawn = false;

                int px = objectsState.getPlayer().getX() * gridWidth / windowWidth;
                int py = objectsState.getPlayer().getY() * gridHeight / windowHeight - 5;
                if (px == x && py == y) {
                    sb.append('P');
                    drawn = true;
                }

                for (GameObject tire : objectsState.getTires()) {
                    int tx = tire.getX() * gridWidth / windowWidth;
                    int ty = tire.getY() * gridHeight / windowHeight;
                    if (tx == x && ty == y) {
                        sb.append('0');
                        drawn = true;
                        break;
                    }
                }

                for (GameObject prize : objectsState.getPrizes()) {
                    int zx = prize.getX() * gridWidth / windowWidth;
                    int zy = prize.getY() * gridHeight / windowHeight;
                    if (zx == x && zy == y) {
                        sb.append('$');
                        drawn = true;
                        break;
                    }
                }

                if (!drawn) {
                    sb.append(' ');
                }
            }
            sb.append('\n');
        }

        Label field = new Label(sb.toString());
        field.setBackgroundColor(TextColor.ANSI.BLACK);
        field.setForegroundColor(TextColor.ANSI.WHITE);
        gamePanel.addComponent(field);

        gamePanel.addComponent(new Label("Жизни: " + objectsState.getPlayer().getLives()).addStyle(SGR.BOLD));
        gamePanel.addComponent(new Label("Очки: " + objectsState.getPlayer().getPoints()).addStyle(SGR.BOLD));
        gui.updateScreen();

        for (int i = 0; i < gridWidth; i++) {
            gamePanel.addComponent(new Label(" "));
        }

        gui.updateScreen();
    }

    @Override
    public void KeyListener(PlayerController controller) {
        new Thread(() -> {
            try {
                while (true) {
                    KeyStroke keyStroke = gui.getScreen().pollInput();
                    if (keyStroke != null) {
                        controller.keyPressedLanterna(keyStroke);
                    }
                }
            } catch (IOException e) {
                System.out.println("Экран закрыт.");
            }
        }).start();
    }

    @Override
    public void modelChanged() throws IOException {
        this.render();
    }
}


