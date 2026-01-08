package ru.nsu.garkusha.ui;

import ru.nsu.garkusha.game.GameConfig;
import ru.nsu.garkusha.game.GameLogic;
import ru.nsu.garkusha.game.GamePlayer;
import ru.nsu.garkusha.game.GameState;
import ru.nsu.garkusha.proto.SnakesProto;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.net.InetAddress;
import java.util.List;

public class MainMenuFrame extends JFrame {
    private GameLogic gameLogic;
    private DefaultListModel<GameInfo> gameListModel;
    private JList<GameInfo> gameList;

    private JTextField gameNameField;
    private JTextField playerNameField;
    private JSpinner widthSpinner;
    private JSpinner heightSpinner;
    private JSpinner foodSpinner;
    private JSpinner delaySpinner;

    private java.util.function.Consumer<List<GameLogic.AnnouncedGame>> gameListListener;

    private static class GameInfo {
        String gameName;
        String masterName;
        int playersCount;
        InetAddress address;
        int port;
        SnakesProto.GameAnnouncement announcement;

        GameInfo(SnakesProto.GameAnnouncement announcement, InetAddress address, int port) {
            this.announcement = announcement;
            this.gameName = announcement.getGameName();

            if (announcement.getPlayers().getPlayersCount() > 0) {
                this.masterName = announcement.getPlayers().getPlayers(0).getName();
            } else {
                this.masterName = "Unknown";
            }

            this.playersCount = announcement.getPlayers().getPlayersCount();
            this.address = address;
            this.port = port;
        }

        @Override
        public String toString() {
            return String.format("%s (Host: %s, Players: %d)",
                    gameName, masterName, playersCount);
        }
    }

    public MainMenuFrame() {
        initComponents();
        setupGameLogic();
        setVisible(true);
    }

    private void initComponents() {
        setTitle("Snakes Game - Main Menu");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(800, 600);
        setLocationRelativeTo(null);

        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
        splitPane.setDividerLocation(400);

        JPanel gamesPanel = createGamesPanel();
        JPanel createGamePanel = createNewGamePanel();

        splitPane.setLeftComponent(gamesPanel);
        splitPane.setRightComponent(createGamePanel);

        add(splitPane);
    }

    private JPanel createGamesPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBorder(BorderFactory.createTitledBorder("Available Games"));

        gameListModel = new DefaultListModel<>();
        gameList = new JList<>(gameListModel);
        gameList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);

        JScrollPane scrollPane = new JScrollPane(gameList);
        panel.add(scrollPane, BorderLayout.CENTER);

        JPanel buttonPanel = new JPanel(new GridLayout(0, 3, 5, 5));

        JButton refreshButton = new JButton("Refresh");
        refreshButton.addActionListener(e -> refreshGameList());

        JButton joinButton = new JButton("Join Game");
        joinButton.addActionListener(e -> joinSelectedGame());

        JButton joinAsViewerButton = new JButton("Join as Viewer");
        joinAsViewerButton.addActionListener(e -> joinAsViewer());

        JButton joinByIpButton = new JButton("Join by IP");
        joinByIpButton.addActionListener(e -> showJoinByIpDialog(false));

        JButton joinByIpViewerButton = new JButton("Join by IP as Viewer");
        joinByIpViewerButton.addActionListener(e -> showJoinByIpDialog(true));

        buttonPanel.add(refreshButton);
        buttonPanel.add(joinButton);
        buttonPanel.add(joinAsViewerButton);
        buttonPanel.add(joinByIpButton);
        buttonPanel.add(joinByIpViewerButton);

        JScrollPane buttonScrollPane = new JScrollPane(buttonPanel);
        buttonScrollPane.setPreferredSize(new Dimension(250, 120));
        buttonScrollPane.setBorder(null);

        panel.add(buttonScrollPane, BorderLayout.SOUTH);

        gameList.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (e.getClickCount() == 2) {
                    joinSelectedGame();
                }
            }
        });

        return panel;
    }

    private void showJoinByIpDialog(boolean asViewer) {
        JDialog dialog = new JDialog(this,
                asViewer ? "Подключиться по IP как Viewer" : "Подключиться по IP как Игрок",
                true);
        dialog.setLayout(new BorderLayout());
        dialog.setSize(400, 200);
        dialog.setLocationRelativeTo(this);

        JPanel mainPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.anchor = GridBagConstraints.WEST;

        gbc.gridx = 0; gbc.gridy = 0;
        mainPanel.add(new JLabel("IP:Порт мастера:"), gbc);
        JTextField ipPortField = new JTextField("192.168.1.1:54321", 20);
        gbc.gridx = 1;
        mainPanel.add(ipPortField, gbc);

        gbc.gridx = 0; gbc.gridy = 1;
        mainPanel.add(new JLabel("Ваше имя:"), gbc);
        JTextField nameField = new JTextField(playerNameField.getText().trim(), 20);
        if (nameField.getText().isEmpty()) {
            nameField.setText("Player" + System.currentTimeMillis() % 10000);
        }
        gbc.gridx = 1;
        mainPanel.add(nameField, gbc);

        gbc.gridx = 0; gbc.gridy = 2; gbc.gridwidth = 2;
        mainPanel.add(new JLabel("Пример: 192.168.56.101:54321"), gbc);

        dialog.add(mainPanel, BorderLayout.CENTER);

        JPanel buttonPanel = new JPanel(new FlowLayout());

        JButton connectButton = new JButton(asViewer ? "Подключиться как Viewer" : "Подключиться как Игрок");
        connectButton.addActionListener(e -> {
            String input = ipPortField.getText().trim();
            String playerName = nameField.getText().trim();

            if (playerName.isEmpty()) {
                JOptionPane.showMessageDialog(dialog,
                        "Введите имя игрока", "Ошибка", JOptionPane.ERROR_MESSAGE);
                return;
            }

            if (!input.matches(".+:\\d+")) {
                JOptionPane.showMessageDialog(dialog,
                        "Неверный формат IP и порта. Пример: 192.168.1.1:54321",
                        "Ошибка", JOptionPane.ERROR_MESSAGE);
                return;
            }

            String[] parts = input.split(":");
            try {
                InetAddress addr = InetAddress.getByName(parts[0].trim());
                int port = Integer.parseInt(parts[1].trim());

                SnakesProto.GameConfig fakeConfig = SnakesProto.GameConfig.newBuilder()
                        .setWidth(40)
                        .setHeight(30)
                        .setFoodStatic(1)
                        .setStateDelayMs(1000)
                        .build();

                SnakesProto.GameAnnouncement fakeAnnouncement = SnakesProto.GameAnnouncement.newBuilder()
                        .setGameName("Direct connect")
                        .setConfig(fakeConfig)
                        .setPlayers(SnakesProto.GamePlayers.getDefaultInstance())
                        .setCanJoin(true)
                        .build();

                SnakesProto.NodeRole role = asViewer ?
                        SnakesProto.NodeRole.VIEWER : SnakesProto.NodeRole.NORMAL;

                gameLogic.joinGame(fakeAnnouncement, playerName, role, addr, port);
                dialog.dispose();

                JOptionPane.showMessageDialog(this,
                        "Пытаемся подключиться к " + input + " как " +
                                (asViewer ? "VIEWER" : "PLAYER") + "...",
                        "Подключение", JOptionPane.INFORMATION_MESSAGE);

            } catch (Exception ex) {
                JOptionPane.showMessageDialog(dialog,
                        "Ошибка подключения: " + ex.getMessage(),
                        "Ошибка", JOptionPane.ERROR_MESSAGE);
            }
        });

        JButton cancelButton = new JButton("Отмена");
        cancelButton.addActionListener(e -> dialog.dispose());

        buttonPanel.add(connectButton);
        buttonPanel.add(cancelButton);

        dialog.add(buttonPanel, BorderLayout.SOUTH);
        dialog.setVisible(true);
    }

    private JPanel createNewGamePanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBorder(BorderFactory.createTitledBorder("Create New Game"));

        JPanel formPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.anchor = GridBagConstraints.WEST;

        gbc.gridx = 0; gbc.gridy = 0;
        formPanel.add(new JLabel("Your Name:"), gbc);
        playerNameField = new JTextField("Player", 15);
        gbc.gridx = 1;
        formPanel.add(playerNameField, gbc);

        gbc.gridx = 0; gbc.gridy = 1;
        formPanel.add(new JLabel("Game Name:"), gbc);
        gameNameField = new JTextField("My Game", 15);
        gbc.gridx = 1;
        formPanel.add(gameNameField, gbc);

        gbc.gridx = 0; gbc.gridy = 2;
        formPanel.add(new JLabel("Field Width:"), gbc);
        widthSpinner = new JSpinner(new SpinnerNumberModel(40, 10, 100, 1));
        gbc.gridx = 1;
        formPanel.add(widthSpinner, gbc);

        gbc.gridx = 0; gbc.gridy = 3;
        formPanel.add(new JLabel("Field Height:"), gbc);
        heightSpinner = new JSpinner(new SpinnerNumberModel(30, 10, 100, 1));
        gbc.gridx = 1;
        formPanel.add(heightSpinner, gbc);

        gbc.gridx = 0; gbc.gridy = 4;
        formPanel.add(new JLabel("Base Food:"), gbc);
        foodSpinner = new JSpinner(new SpinnerNumberModel(1, 0, 100, 1));
        gbc.gridx = 1;
        formPanel.add(foodSpinner, gbc);

        gbc.gridx = 0; gbc.gridy = 5;
        formPanel.add(new JLabel("Turn Delay (ms):"), gbc);
        delaySpinner = new JSpinner(new SpinnerNumberModel(500, 100, 3000, 100));
        gbc.gridx = 1;
        formPanel.add(delaySpinner, gbc);

        panel.add(formPanel, BorderLayout.CENTER);

        JButton createButton = new JButton("Create Game");
        createButton.addActionListener(e -> createNewGame());
        createButton.setPreferredSize(new Dimension(200, 40));

        JPanel buttonPanel = new JPanel();
        buttonPanel.add(createButton);
        panel.add(buttonPanel, BorderLayout.SOUTH);

        return panel;
    }

    private void setupGameLogic() {
        gameLogic = new GameLogic();

        gameLogic.setGameListListener(this::updateGameList);

        gameLogic.setStateListener(new GameLogic.GameStateListener() {
            @Override
            public void onGameStateUpdated(GameState state) {
                SwingUtilities.invokeLater(MainMenuFrame.this::openGameWindow);
            }

            @Override
            public void onPlayerListUpdated(List<GamePlayer> players) {}

            @Override
            public void onErrorMessage(String message) {
                SwingUtilities.invokeLater(() ->
                        JOptionPane.showMessageDialog(MainMenuFrame.this, message, "Error", JOptionPane.ERROR_MESSAGE)
                );
            }
        });

        new Timer(2000, e -> refreshGameList()).start();
        gameLogic.startDiscovery();
    }

    private void updateGameList(List<GameLogic.AnnouncedGame> games) {
        SwingUtilities.invokeLater(() -> {
            gameListModel.clear();
            for (GameLogic.AnnouncedGame ag : games) {
                GameInfo info = new GameInfo(ag.announcement(), ag.address(), ag.port());
                gameListModel.addElement(info);
            }
        });
    }

    private void refreshGameList() {
        System.out.println("Discovering games via multicast...");
    }

    private void joinSelectedGame() {
        GameInfo selected = gameList.getSelectedValue();
        if (selected == null) {
            JOptionPane.showMessageDialog(this, "Please select a game first", "Error", JOptionPane.WARNING_MESSAGE);
            return;
        }

        String playerName = playerNameField.getText().trim();
        if (playerName.isEmpty()) {
            playerName = "Player" + (System.currentTimeMillis() % 10000);
        }

        gameLogic.joinGame(selected.announcement, playerName,
                SnakesProto.NodeRole.NORMAL, selected.address, selected.port);

        JOptionPane.showMessageDialog(this,
                "Joining game: " + selected.gameName, "Connecting...", JOptionPane.INFORMATION_MESSAGE);
    }

    private void joinAsViewer() {
        GameInfo selected = gameList.getSelectedValue();
        if (selected == null) {
            JOptionPane.showMessageDialog(this, "Please select a game first", "Error", JOptionPane.WARNING_MESSAGE);
            return;
        }

        String playerName = JOptionPane.showInputDialog(this, "Enter your name:", "Viewer", JOptionPane.PLAIN_MESSAGE);
        if (playerName != null && !playerName.trim().isEmpty()) {
            gameLogic.joinGame(selected.announcement, playerName,
                    SnakesProto.NodeRole.VIEWER, selected.address, selected.port);
        }
    }

    private void createNewGame() {
        String playerName = playerNameField.getText().trim();
        String gameName = gameNameField.getText().trim();

        if (playerName.isEmpty() || gameName.isEmpty()) {
            JOptionPane.showMessageDialog(this,
                    "Enter player name and game name", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        GameConfig config = new GameConfig(
                (Integer) widthSpinner.getValue(),
                (Integer) heightSpinner.getValue(),
                (Integer) foodSpinner.getValue(),
                (Integer) delaySpinner.getValue()
        );

        gameLogic.startNewGame(config, gameName, playerName);
    }

    private void openGameWindow() {
        for (Window window : Window.getWindows()) {
            if (window instanceof GameFrame) {
                window.toFront();
                return;
            }
        }

        setVisible(false);

        GameFrame gameFrame = new GameFrame(gameLogic);
        gameFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        gameFrame.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosed(WindowEvent e) {
                gameLogic.stopGame();
                setVisible(true);
            }
        });
        gameFrame.setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            } catch (Exception ignored) {}
            new MainMenuFrame();
        });
    }
}