package ru.nsu.garkusha.ui;

import ru.nsu.garkusha.game.GameLogic;
import ru.nsu.garkusha.game.GameState;
import ru.nsu.garkusha.game.GamePlayer;
import ru.nsu.garkusha.proto.SnakesProto;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.List;


public class GameFrame extends JFrame {
    private GameLogic gameLogic;
    private GamePanel gamePanel;
    private PlayersPanel playersPanel;
    private JLabel statusLabel;

    public GameFrame(GameLogic gameLogic) {
        this.gameLogic = gameLogic;
        initComponents();
        setupGameLogicListeners();
        setupKeyboardControls();

        setTitle("Snakes Game - " + gameLogic.getGameName());
        pack();
        setLocationRelativeTo(null);
    }

    private void initComponents() {
        setLayout(new BorderLayout());

        gamePanel = new GamePanel(gameLogic);
        add(gamePanel, BorderLayout.CENTER);

        JPanel rightPanel = new JPanel(new BorderLayout());
        rightPanel.setPreferredSize(new Dimension(250, 0));

        playersPanel = new PlayersPanel();
        rightPanel.add(playersPanel, BorderLayout.CENTER);

        JPanel bottomPanel = new JPanel(new BorderLayout());

        statusLabel = new JLabel("Status: " + getRoleString(gameLogic.getRole()));
        bottomPanel.add(statusLabel, BorderLayout.WEST);

        JButton exitButton = new JButton("Exit Game");
        exitButton.addActionListener(e -> exitGame());
        bottomPanel.add(exitButton, BorderLayout.EAST);

        rightPanel.add(bottomPanel, BorderLayout.SOUTH);

        add(rightPanel, BorderLayout.EAST);

        int fieldWidth = gameLogic.getConfig().getWidth();
        int fieldHeight = gameLogic.getConfig().getHeight();
        int cellSize = 20;

        setPreferredSize(new Dimension(
                fieldWidth * cellSize + 300,
                fieldHeight * cellSize + 100
        ));
    }

    private String getRoleString(SnakesProto.NodeRole role) {
        switch (role) {
            case MASTER: return "MASTER";
            case NORMAL: return "PLAYER";
            case VIEWER: return "VIEWER";
            case DEPUTY: return "DEPUTY";
            default: return "UNKNOWN";
        }
    }

    private void setupGameLogicListeners() {
        gameLogic.setStateListener(new GameLogic.GameStateListener() {
            @Override
            public void onGameStateUpdated(GameState state) {
                SwingUtilities.invokeLater(() -> {
                    gamePanel.updateGameState(state);
                    gamePanel.repaint();

                    statusLabel.setText(String.format("Status: %s | Turn: %d",
                            getRoleString(gameLogic.getRole()), state.getStateOrder()));
                });
            }

            @Override
            public void onPlayerListUpdated(List<GamePlayer> players) {
                SwingUtilities.invokeLater(() -> {
                    playersPanel.updatePlayers(players);
                });
            }

            @Override
            public void onErrorMessage(String message) {
                SwingUtilities.invokeLater(() -> {
                    JOptionPane.showMessageDialog(GameFrame.this,
                            message, "Game Error", JOptionPane.ERROR_MESSAGE);
                });
            }
        });
    }

    private void setupKeyboardControls() {
        gamePanel.setFocusable(true);
        gamePanel.requestFocusInWindow();

        InputMap inputMap = gamePanel.getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW);
        ActionMap actionMap = gamePanel.getActionMap();

        setupKeyAction(inputMap, actionMap, KeyEvent.VK_W, "up", SnakesProto.Direction.UP);
        setupKeyAction(inputMap, actionMap, KeyEvent.VK_S, "down", SnakesProto.Direction.DOWN);
        setupKeyAction(inputMap, actionMap, KeyEvent.VK_A, "left", SnakesProto.Direction.LEFT);
        setupKeyAction(inputMap, actionMap, KeyEvent.VK_D, "right", SnakesProto.Direction.RIGHT);

        setupKeyAction(inputMap, actionMap, KeyEvent.VK_UP, "arrow_up", SnakesProto.Direction.UP);
        setupKeyAction(inputMap, actionMap, KeyEvent.VK_DOWN, "arrow_down", SnakesProto.Direction.DOWN);
        setupKeyAction(inputMap, actionMap, KeyEvent.VK_LEFT, "arrow_left", SnakesProto.Direction.LEFT);
        setupKeyAction(inputMap, actionMap, KeyEvent.VK_RIGHT, "arrow_right", SnakesProto.Direction.RIGHT);

        gamePanel.addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                handleKeyPress(e.getKeyCode());
            }
        });
    }
    private void setupKeyAction(InputMap inputMap, ActionMap actionMap,
                                int keyCode, String actionName,
                                final SnakesProto.Direction direction) {
        KeyStroke keyStroke = KeyStroke.getKeyStroke(keyCode, 0);
        inputMap.put(keyStroke, actionName);

        actionMap.put(actionName, new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                sendSteerCommand(direction);
            }
        });
    }
    private void handleKeyPress(int keyCode) {
        SnakesProto.Direction direction = null;

        switch (keyCode) {
            case KeyEvent.VK_W:
            case KeyEvent.VK_UP:
                direction = SnakesProto.Direction.UP;
                break;
            case KeyEvent.VK_S:
            case KeyEvent.VK_DOWN:
                direction = SnakesProto.Direction.DOWN;
                break;
            case KeyEvent.VK_A:
            case KeyEvent.VK_LEFT:
                direction = SnakesProto.Direction.LEFT;
                break;
            case KeyEvent.VK_D:
            case KeyEvent.VK_RIGHT:
                direction = SnakesProto.Direction.RIGHT;
                break;
        }

        if (direction != null) {
            sendSteerCommand(direction);
        }
    }

    private void sendSteerCommand(SnakesProto.Direction direction) {
        System.out.println("Key pressed: sending steer command " + direction +
                " for player " + gameLogic.getPlayerId());
        gameLogic.sendSteerCommand(direction);
    }

    private void exitGame() {
        int confirm = JOptionPane.showConfirmDialog(this,
                "Are you sure you want to exit the game?",
                "Exit Game", JOptionPane.YES_NO_OPTION);

        if (confirm == JOptionPane.YES_OPTION) {
            dispose();
        }
    }

    @Override
    public void dispose() {
        gameLogic.stopGame();
        super.dispose();
    }
}