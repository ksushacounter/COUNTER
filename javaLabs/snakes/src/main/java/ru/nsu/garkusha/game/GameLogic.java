package ru.nsu.garkusha.game;

import ru.nsu.garkusha.proto.SnakesProto;
import ru.nsu.garkusha.network.NetworkManager;

import javax.swing.*;
import java.net.InetSocketAddress;
import java.util.*;
import java.util.concurrent.*;
import java.net.InetAddress;
import java.util.Random;

public class GameLogic {
    private GameState currentState;
    private GameConfig config;
    private String gameName;
    private String playerName;
    private int playerId;
    private SnakesProto.NodeRole role;
    private InetAddress masterAddress;
    private int masterPort;

    private NetworkManager networkManager;

    private final Map<Integer, InetSocketAddress> playerAddresses;
    private final Map<Integer, Long> playerLastSeen;
    private final Map<Integer, PendingSteer> pendingSteers;
    private int deputyId;

    private ScheduledExecutorService gameLoopExecutor;
    private ScheduledFuture<?> gameLoopFuture;
    private ScheduledFuture<?> announcementFuture;

    private GameStateListener stateListener;
    private GameListListener gameListListener;
    private final Random random;

    private final Map<Long, SnakesProto.GameMessage> pendingMessages;
    private final List<SnakesProto.GameAnnouncement> availableGames;
    private long lastJoinMsgSeq = -1;


    public interface GameStateListener {
        void onGameStateUpdated(GameState state);

        void onPlayerListUpdated(List<GamePlayer> players);

        void onErrorMessage(String message);
    }

    public interface GameListListener {
        void onGameListUpdated(List<AnnouncedGame> games);
    }


    private static class PendingSteer {
        SnakesProto.Direction direction;
        long msgSeq;
        long timestamp;

        PendingSteer(SnakesProto.Direction direction, long msgSeq) {
            this.direction = direction;
            this.msgSeq = msgSeq;
            this.timestamp = System.currentTimeMillis();
        }
    }

    public GameLogic() {
        this.playerAddresses = new ConcurrentHashMap<>();
        this.playerLastSeen = new ConcurrentHashMap<>();
        this.pendingSteers = new ConcurrentHashMap<>();
        this.pendingMessages = new ConcurrentHashMap<>();
        this.availableGames = new ArrayList<>();
        this.random = new Random();
        this.deputyId = -1;
    }


    public void startNewGame(GameConfig config, String gameName, String playerName) {
        this.config = config;
        this.gameName = gameName;
        this.playerName = playerName;
        this.role = SnakesProto.NodeRole.MASTER;
        this.playerId = 1;

        createInitialGameState();

        try {
            networkManager = new NetworkManager(this::handleNetworkMessage);
            networkManager.start(config.getStateDelayMs());

            startGameLoop();

            startAnnouncements();

            System.out.println("New game started as MASTER: " + gameName);

        } catch (Exception e) {
            if (stateListener != null) {
                stateListener.onErrorMessage("Failed to start game: " + e.getMessage());
            }
        }
    }

    public void startDiscovery() {
        if (networkManager != null) return;

        try {
            networkManager = new NetworkManager(this::handleNetworkMessage);
            networkManager.start(1000);
            System.out.println("Discovery mode started: Listening for Multicast...");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void joinGame(SnakesProto.GameAnnouncement game, String playerName, SnakesProto.NodeRole requestedRole, InetAddress masterAddress, int masterPort) {
        this.config = new GameConfig(game.getConfig());
        this.gameName = game.getGameName();
        this.playerName = playerName;
        this.role = requestedRole;
        this.masterAddress = masterAddress;
        this.masterPort = masterPort;
        this.playerId = -1;
        this.lastJoinMsgSeq = -1;

        try {
            networkManager = new NetworkManager(this::handleNetworkMessage);
            networkManager.start(config.getStateDelayMs());

            SnakesProto.GameMessage joinMsg = networkManager.createJoinMsg(playerName, gameName, requestedRole);
            this.lastJoinMsgSeq = joinMsg.getMsgSeq();
            networkManager.sendUnicast(joinMsg, masterAddress, masterPort);
            System.out.println(this.playerId);

            System.out.println("Joining game: " + gameName);

            if (stateListener != null) {
                SwingUtilities.invokeLater(() -> {
                    stateListener.onErrorMessage("Attempting to join game...");
                });
            }
        } catch (Exception e) {
            System.err.println("Failed to join game: " + e.getMessage());
            if (stateListener != null) {
                stateListener.onErrorMessage("Failed to join game: " + e.getMessage());
            }
        }

    }

    private void createInitialGameState() {
        List<GamePlayer> players = new ArrayList<>();
        players.add(new GamePlayer(playerName, playerId, role, 0));

        List<Snake> snakes = new ArrayList<>();
        Snake masterSnake = createInitialSnake(playerId);
        snakes.add(masterSnake);

        Set<Coord> foods = generateInitialFood(snakes);

        currentState = new GameState(0, snakes, foods, players);
    }

    private Snake createInitialSnake(int playerId) {
        int centerX = config.getWidth() / 2;
        int centerY = config.getHeight() / 2;

        List<Coord> points = new ArrayList<>();
        points.add(new Coord(centerX, centerY));
        points.add(new Coord(0, 1));
        Snake snake = new Snake(playerId, points, SnakesProto.GameState.Snake.SnakeState.ALIVE, SnakesProto.Direction.UP);

        return snake;
    }

    private Set<Coord> generateInitialFood(List<Snake> snakes) {
        Set<Coord> foods = new HashSet<>();
        int totalFood = config.getFoodStatic() + snakes.size();

        System.out.println("Generating initial food: need " + totalFood + " (static: " + config.getFoodStatic() + " + snakes: " + snakes.size() + ")");

        while (foods.size() < totalFood) {
            Coord food = generateRandomFood(snakes, foods);
            if (food != null) {
                foods.add(food);
                System.out.println("  Initial food placed at: " + food);
            } else {
                System.err.println("  WARNING: Could not place all initial food!");
                break;
            }
        }

        System.out.println("Generated " + foods.size() + " initial food items");
        return foods;
    }


    private Coord generateRandomFood(List<Snake> snakes, Set<Coord> existingFoods) {
        if (config == null) {
            return null;
        }

        int width = config.getWidth();
        int height = config.getHeight();
        int maxAttempts = width * height * 3;

        System.out.println("  Looking for free cell for food...");

        for (int i = 0; i < maxAttempts; i++) {
            int x = random.nextInt(width);
            int y = random.nextInt(height);
            Coord coord = new Coord(x, y);

            boolean occupiedBySnake = false;
            for (Snake snake : snakes) {
                if (snake.contains(coord, width, height)) {
                    occupiedBySnake = true;
                    break;
                }
            }

            if (occupiedBySnake) {
                continue;
            }

            boolean occupiedByFood = existingFoods.contains(coord);

            if (!occupiedByFood) {
                System.out.println("    Found free cell at: " + coord + " (attempt " + (i + 1) + ")");
                return coord;
            }
        }

        System.err.println("    ERROR: Could not find free cell after " + maxAttempts + " attempts");
        return null;
    }

    private void startGameLoop() {
        if (role != SnakesProto.NodeRole.MASTER) {
            return;
        }

        if (gameLoopFuture != null && !gameLoopFuture.isCancelled()) {
            return;
        }

        if (gameLoopExecutor == null) {
            gameLoopExecutor = Executors.newSingleThreadScheduledExecutor();
        }

        gameLoopFuture = gameLoopExecutor.scheduleAtFixedRate(() -> {
            try {
                gameTick();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }, config.getStateDelayMs(), config.getStateDelayMs(), TimeUnit.MILLISECONDS);
    }

    private void handleNetworkMessage(SnakesProto.GameMessage message, InetAddress senderAddress, int senderPort) {
//        if (!message.hasAck() && !message.hasPing()) {
//            networkManager.sendAck(message.getMsgSeq(), playerId, message.getSenderId(), senderAddress, senderPort);
//        }
//        if (message.getMsgSeq() == -888) {
//            InetSocketAddress timeoutAddress = new InetSocketAddress(senderAddress, senderPort);
//            Integer timeoutPlayerId = findPlayerIdByAddress(timeoutAddress);
//
//            if (timeoutPlayerId != null) {
//                GamePlayer timeoutPlayer = currentState.getPlayerById(timeoutPlayerId);
//                if (timeoutPlayer != null && timeoutPlayer.isMaster()) {
//                    System.out.println("MASTER timed out! ID: " + timeoutPlayerId);
//
//                    if (role == SnakesProto.NodeRole.DEPUTY) {
//                        System.out.println("DEPUTY should become MASTER now!");
//                        becomeMaster();
//                    } else if (role == SnakesProto.NodeRole.NORMAL) {
//                        System.out.println("NORMAL player should redirect to DEPUTY!");
//                        redirectToDeputy();
//                    }
//                } else {
//                    convertPlayerToZombie(timeoutPlayerId);
//                }
//            } else {
//                System.out.println("Timeout from unknown address: " + timeoutAddress);
//            }
//            return;
//        }
        if (!message.hasAck() && !message.hasPing()) {
            networkManager.sendAck(message.getMsgSeq(), playerId, message.getSenderId(), senderAddress, senderPort);
        }

        if (message.getMsgSeq() == -888) {
            InetSocketAddress timeoutAddress = new InetSocketAddress(senderAddress, senderPort);
            Integer timeoutPlayerId = findPlayerIdByAddress(timeoutAddress);

            System.out.println("[TIMEOUT] Processing timeout for address: " + timeoutAddress);

            if (timeoutPlayerId != null) {
                GamePlayer timeoutPlayer = currentState.getPlayerById(timeoutPlayerId);
                if (timeoutPlayer != null) {
                    System.out.println("[TIMEOUT] Player ID " + timeoutPlayerId +
                            " (" + timeoutPlayer.getName() + ") timed out. Role: " + timeoutPlayer.getRole());

                    if (timeoutPlayer.isMaster()) {
                        System.out.println("[TIMEOUT] MASTER timed out! ID: " + timeoutPlayerId);

                        if (role == SnakesProto.NodeRole.MASTER) {
                            System.out.println("[TIMEOUT] We are already MASTER, ignoring");
                            return;
                        }

                        if (role == SnakesProto.NodeRole.DEPUTY) {
                            System.out.println("[TIMEOUT] DEPUTY should become MASTER now!");
                            becomeMaster();
                        } else if (role == SnakesProto.NodeRole.NORMAL) {
                            System.out.println("[TIMEOUT] NORMAL player should redirect to DEPUTY!");
                            redirectToDeputy();
                        }
                    } else {
                        System.out.println("[TIMEOUT] Non-master player timed out, converting to zombie");
                        convertPlayerToZombie(timeoutPlayerId);
                    }
                } else {
                    System.out.println("[TIMEOUT] Player with ID " + timeoutPlayerId + " not found in game state");
                }
            } else {
                System.out.println("[TIMEOUT] Timeout from unknown address: " + timeoutAddress);

                if (masterAddress != null &&
                        masterAddress.equals(senderAddress) &&
                        masterPort == senderPort) {
                    System.out.println("[TIMEOUT] This is our MASTER address! Master has disconnected.");

                    if (role == SnakesProto.NodeRole.DEPUTY) {
                        System.out.println("[TIMEOUT] DEPUTY detecting master disconnect, becoming MASTER");
                        becomeMaster();
                    } else if (role == SnakesProto.NodeRole.NORMAL) {
                        System.out.println("[TIMEOUT] NORMAL player detecting master disconnect, redirecting");
                        redirectToDeputy();
                    }
                }
            }
            return;
        }
        if (message.hasPing()) {
            handlePing(message, senderAddress, senderPort);
        } else if (message.hasAck()) {
            handleAck(message);
        } else if (message.hasState()) {
            handleState(message);
        } else if (message.hasAnnouncement()) {
            handleAnnouncement(message, senderAddress, senderPort);
        } else if (message.hasJoin()) {
            handleJoin(message, senderAddress, senderPort);
        } else if (message.hasSteer()) {
            handleSteer(message);
        } else if (message.hasError()) {
            handleError(message);
        } else if (message.hasRoleChange()) {
            handleRoleChange(message);
        }
    }

    private void becomeMaster() { // депути когда умирает/выходит заменяется нормально, мастер когда умирает все ок, но стир месаги не уходят, если же прога мастера прерывается - все виснет
        System.out.println("DEPUTY becoming MASTER due to timeout");

        role = SnakesProto.NodeRole.MASTER;
        deputyId = -1;

        if (gameLoopExecutor == null) {
            gameLoopExecutor = Executors.newSingleThreadScheduledExecutor();
        }

        playerAddresses.clear();

        for (GamePlayer player : currentState.getPlayers()) {
            if (player.getIpAddress() != null && !player.getIpAddress().isEmpty()) {
                try {
                    InetAddress addr = InetAddress.getByName(player.getIpAddress());
                    InetSocketAddress socketAddr = new InetSocketAddress(addr, player.getPort());
                    playerAddresses.put(player.getId(), socketAddr);
                    playerLastSeen.put(player.getId(), System.currentTimeMillis());
                    System.out.println("Added player " + player.getId() + " address: " + socketAddr);
                } catch (Exception e) {
                    System.err.println("Failed to parse address for player " + player.getId() + ": " + e.getMessage());
                }
            }
        }

        updatePlayerRole(playerId, SnakesProto.NodeRole.MASTER);

        selectNewDeputy();

        startGameLoop();

        startAnnouncements();

        masterAddress = null;
        masterPort = 0;

        System.out.println("Successfully became MASTER. Players known: " + playerAddresses.size());

        if (stateListener != null) {
            SwingUtilities.invokeLater(() -> {
                stateListener.onErrorMessage("You are now the MASTER (previous master disconnected)");
            });
        }

        broadcastGameState();
    }


    private void redirectToDeputy() {
        if (currentState == null) return;

        for (GamePlayer player : currentState.getPlayers()) {
            if (player.isDeputy()) {
                deputyId = player.getId();
                try {
                    masterAddress = InetAddress.getByName(player.getIpAddress());
                    masterPort = player.getPort();
                    System.out.println("Redirecting to DEPUTY " + deputyId + " at " + masterAddress + ":" + masterPort);
                    return;
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }

        for (GamePlayer player : currentState.getPlayers()) {
            if (player.getId() != playerId && !player.isViewer() && !player.isMaster()) {
                deputyId = player.getId();
                try {
                    masterAddress = InetAddress.getByName(player.getIpAddress());
                    masterPort = player.getPort();
                    System.out.println("No DEPUTY found, redirecting to player " + deputyId);
                    break;
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }


    private void handleJoin(SnakesProto.GameMessage message, InetAddress senderAddress, int senderPort) {
        if (role != SnakesProto.NodeRole.MASTER) {
            return;
        }

        System.out.println("Handling join request from " + message.getJoin().getPlayerName() +
                " at " + senderAddress + ":" + senderPort +
                " (msg_seq=" + message.getMsgSeq() + ")");

        Integer existingPlayerId = findPlayerIdByAddress(new InetSocketAddress(senderAddress, senderPort));
        if (existingPlayerId != null) {
            System.out.println("Player already exists with ID: " + existingPlayerId +
                    ", sending ACK instead of creating new player");
            sendJoinAck(existingPlayerId, senderAddress, senderPort, message.getMsgSeq());
            return;
        }

        int newPlayerId = generatePlayerId();

        GamePlayer newPlayer = new GamePlayer(message.getJoin().getPlayerName(), newPlayerId,
                senderAddress.getHostAddress(), senderPort,
                message.getJoin().getRequestedRole(),
                SnakesProto.PlayerType.HUMAN, 0);

        List<GamePlayer> updatedPlayers = new ArrayList<>(currentState.getPlayers());

        boolean isViewer = message.getJoin().getRequestedRole() == SnakesProto.NodeRole.VIEWER;
        System.out.println("Requested role: " + message.getJoin().getRequestedRole());

        Snake newSnake = createSnakeForNewPlayer(newPlayerId, isViewer);
        if (newSnake == null) {
            System.err.println("No space for new snake, rejecting player");
            sendJoinError("No space for new snake", senderAddress, senderPort, message.getMsgSeq());
            return;
        }

        List<Snake> updatedSnakes = new ArrayList<>(currentState.getSnakes());
        updatedSnakes.add(newSnake);

        GamePlayer playerToAdd = newPlayer;
        if (deputyId == -1 && newPlayer.getRole() == SnakesProto.NodeRole.NORMAL) {
            deputyId = newPlayerId;
            playerToAdd = newPlayer.withRole(SnakesProto.NodeRole.DEPUTY);
            sendRoleChange(newPlayerId, SnakesProto.NodeRole.DEPUTY, senderAddress, senderPort);
            System.out.println("New player " + newPlayerId + " has been appointed as DEPUTY");
        }

        updatedPlayers.add(playerToAdd);

        currentState = new GameState(currentState.getStateOrder(), updatedSnakes,
                currentState.getFoods(), updatedPlayers);

        playerAddresses.put(newPlayerId, new InetSocketAddress(senderAddress, senderPort));
        playerLastSeen.put(newPlayerId, System.currentTimeMillis());

        sendJoinAck(newPlayerId, senderAddress, senderPort, message.getMsgSeq());

        System.out.println("Player joined: " + playerToAdd.getName() +
                " (ID: " + newPlayerId + ", Role: " + playerToAdd.getRole() + ")");

        broadcastGameState();
    }

    private Snake createSnakeForNewPlayer(int playerId, boolean isViewer) {
        Coord headPos = findSpawnPoint();
        if (headPos == null) {
            return null;
        }

        List<Coord> points = new ArrayList<>();
        points.add(headPos);
        points.add(new Coord(0, 1));

        SnakesProto.GameState.Snake.SnakeState initialState = isViewer ? SnakesProto.GameState.Snake.SnakeState.ZOMBIE : SnakesProto.GameState.Snake.SnakeState.ALIVE;

        Snake newSnake = new Snake(playerId, points, initialState, SnakesProto.Direction.UP);

        if (isViewer) {
            updatePlayerRole(playerId, SnakesProto.NodeRole.VIEWER);
        }

        return newSnake;
    }


    private Coord findSpawnPoint() {
        int width = config.getWidth();
        int height = config.getHeight();

        for (int centerY = 0; centerY < height; centerY++) {
            for (int centerX = 0; centerX < width; centerX++) {
                if (isSquareFree(centerX, centerY, 5)) {
                    return new Coord(centerX, centerY);
                }
            }
        }

        return null;
    }


    private boolean isSquareFree(int centerX, int centerY, int size) {
        int halfSize = size / 2;
        List<Snake> snakes = currentState.getSnakes();

        for (int dy = -halfSize; dy <= halfSize; dy++) {
            for (int dx = -halfSize; dx <= halfSize; dx++) {
                int x = (centerX + dx + config.getWidth()) % config.getWidth();
                int y = (centerY + dy + config.getHeight()) % config.getHeight();
                Coord coord = new Coord(x, y);

                for (Snake snake : snakes) {
                    if (snake.contains(coord, config.getWidth(), config.getHeight())) {
                        return false;
                    }
                }

                if (currentState.isFoodAt(coord)) {
                    return false;
                }
            }
        }

        return true;
    }

    private void sendJoinAck(int newPlayerId, InetAddress address, int port, long msgSeq) {
        SnakesProto.GameMessage ackMsg = SnakesProto.GameMessage.newBuilder().setMsgSeq(msgSeq).setSenderId(playerId).setReceiverId(newPlayerId).setAck(SnakesProto.GameMessage.AckMsg.newBuilder().build()).build();

        networkManager.sendUnicast(ackMsg, address, port);
        System.out.println("Sent Join ACK with receiver_id = " + newPlayerId + " (msg_seq=" + msgSeq + ")");
    }


    private void sendJoinError(String errorMessage, InetAddress address, int port, long msgSeq) {
        SnakesProto.GameMessage errorMsg = SnakesProto.GameMessage.newBuilder().setMsgSeq(msgSeq).setError(SnakesProto.GameMessage.ErrorMsg.newBuilder().setErrorMessage(errorMessage).build()).build();

        networkManager.sendUnicast(errorMsg, address, port);
    }


    private void gameTick() {
        try {
            if (currentState == null) {
                return;
            }
            applyPendingSteers();

            moveAllSnakes();
            checkCollisions();
            updateFood();

            currentState = new GameState(currentState.getStateOrder() + 1, currentState.getSnakes(), currentState.getFoods(), currentState.getPlayers());

            broadcastGameState();

            if (stateListener != null) {
                stateListener.onGameStateUpdated(currentState);
                stateListener.onPlayerListUpdated(currentState.getPlayers());
            }

        } catch (Exception e) {
            System.err.println("Error in gameTick: " + e.getMessage());
            e.printStackTrace();
        }
    }


    private void applyPendingSteers() {
        for (Map.Entry<Integer, PendingSteer> entry : pendingSteers.entrySet()) {
            int playerId = entry.getKey();
            PendingSteer steer = entry.getValue();

            Snake snake = currentState.getSnakeByPlayerId(playerId);
            if (snake != null && snake.getState() == SnakesProto.GameState.Snake.SnakeState.ALIVE) {
                snake.setDirection(steer.direction, config.getWidth(), config.getHeight());
            }
            System.out.println("22222222222222222222222222222222222222222222222222222222222222222222222222222222");
        }

        pendingSteers.clear();
    }


    private void moveAllSnakes() {
        if (currentState == null || config == null) {
            return;
        }

        List<Snake> snakes = currentState.getSnakes();
        Set<Coord> foods = new HashSet<>(currentState.getFoods());
        List<Coord> freedCells = new ArrayList<>();

        System.out.println("=== MOVING SNAKES ===");
        System.out.println("Food on field: " + foods.size());

        for (Snake snake : snakes) {
            if (snake == null) {
                continue;
            }

            try {
                Coord currentHead = snake.getHead(config.getWidth(), config.getHeight());
                SnakesProto.Direction direction = snake.getHeadDirection();

                Coord newHead = currentHead.move(direction).normalize(config.getWidth(), config.getHeight());

                boolean eatFood = foods.contains(newHead);

                Coord freedCell = snake.moveSimple(eatFood, config.getWidth(), config.getHeight());
                if (freedCell != null) {
                    freedCells.add(freedCell);
                    System.out.println("  Freed cell: " + freedCell);
                }

                if (eatFood) {
                    foods.remove(newHead);
                    increasePlayerScore(snake.getPlayerId(), 1);
                }

            } catch (Exception e) {
                System.err.println("Error moving snake for player " + snake.getPlayerId() + ": " + e.getMessage());
                e.printStackTrace();
            }
        }

        currentState = new GameState(currentState.getStateOrder(), snakes, foods, currentState.getPlayers());

        System.out.println("Food left after moving: " + foods.size());
        System.out.println("=== END MOVING SNAKES ===");
    }


    private void checkCollisions() {
        List<Snake> snakes = currentState.getSnakes();
        List<Snake> deadSnakes = new ArrayList<>();
        Set<Coord> newFoods = new HashSet<>();

        for (Snake snake : snakes) {
//            if (snake.getState() != SnakesProto.GameState.Snake.SnakeState.ALIVE) {
//                continue;
//            }

            Coord head = snake.getHead(config.getWidth(), config.getHeight());
            boolean collision = false;

            if (snake.isSelfCollision(config.getWidth(), config.getHeight())) {
                collision = true;
            }

            for (Snake otherSnake : snakes) {
                if (otherSnake.getPlayerId() == snake.getPlayerId()) {
                    continue;
                }

                if (otherSnake.contains(head, config.getWidth(), config.getHeight())) {
                    collision = true;
                    increasePlayerScore(otherSnake.getPlayerId(), 1);
                    break;
                }
            }

            for (Snake otherSnake : snakes) {
                if (otherSnake.getPlayerId() == snake.getPlayerId()) {
                    continue;
                }

                Coord otherHead = otherSnake.getHead(config.getWidth(), config.getHeight());
                if (head.equals(otherHead)) {
                    if (!deadSnakes.contains(snake)) {
                        deadSnakes.add(snake);
                    }
                    if (!deadSnakes.contains(otherSnake)) {
                        deadSnakes.add(otherSnake);
                    }
                }
            }

            if (collision && !deadSnakes.contains(snake)) {
                deadSnakes.add(snake);
            }
        }

        List<Snake> updatedSnakes = new ArrayList<>(snakes);

        for (Snake deadSnake : deadSnakes) {
            List<Coord> segments = deadSnake.getAllSegments(config.getWidth(), config.getHeight());
            updatedSnakes.remove(deadSnake);
            removePlayer(deadSnake.getPlayerId());


            for (Coord segment : segments) {
                if (random.nextDouble() < 0.5) {
                    boolean cellOccupied = false;

                    if (currentState.isFoodAt(segment)) {
                        cellOccupied = true;
                    }
                    if (!cellOccupied) {
                        for (Snake otherSnake : updatedSnakes) {
                            if (otherSnake.contains(segment, config.getWidth(), config.getHeight())) {
                                cellOccupied = true;
                                break;
                            }
                        }
                    }
                    if (!cellOccupied) {
                        newFoods.add(segment);
                    }
                }
            }

            System.out.println("Snake " + deadSnake.getPlayerId() + " died. " + "Created " + newFoods.size() + " food from its segments.");
        }

        Set<Coord> currentFoods = new HashSet<>(currentState.getFoods());
        currentFoods.addAll(newFoods);

        List<GamePlayer> updatedPlayers = new ArrayList<>();
        for (GamePlayer player : currentState.getPlayers()) {
            boolean isAlive = false;
            for (Snake snake : updatedSnakes) {
                if (snake.getPlayerId() == player.getId()) {
                    isAlive = true;
                    break;
                }
            }
            if (isAlive) {
                updatedPlayers.add(player);
            }
        }

        currentState = new GameState(currentState.getStateOrder(), updatedSnakes, currentFoods, updatedPlayers);
    }

    private void removePlayer(int playerId) {
        List<GamePlayer> players = new ArrayList<>(currentState.getPlayers());
        List<GamePlayer> updatedPlayers = new ArrayList<>();

        boolean wasMaster = false;
        boolean wasDeputy = false;

        for (GamePlayer player : players) {
            if (player.getId() == playerId) {
                if (player.isMaster()) {
                    wasMaster = true;
                }
                if (player.getId() == deputyId) {
                    wasDeputy = true;
                }
            } else {
                updatedPlayers.add(player);
            }
        }

        currentState = new GameState(currentState.getStateOrder(), currentState.getSnakes(), currentState.getFoods(), updatedPlayers);

        if (wasMaster) {
            System.out.println("MASTER removed. Handling master replacement...");

            if (role == SnakesProto.NodeRole.MASTER) {
                deputyId = -1;
                selectNewDeputy();
            } else if (role == SnakesProto.NodeRole.DEPUTY) {
                becomeMaster();
            } else if (wasDeputy) {
                deputyId = -1;
                selectNewDeputy();
            }
        }
    }

    private void convertPlayerToZombie(int playerId) {
        if (currentState == null) return;

        List<Snake> snakes = currentState.getSnakes();
        List<Snake> updatedSnakes = new ArrayList<>();

        for (Snake snake : snakes) {
            if (snake.getPlayerId() == playerId) {
                snake.setState(SnakesProto.GameState.Snake.SnakeState.ZOMBIE);
                updatedSnakes.add(snake);

                updatePlayerRole(playerId, SnakesProto.NodeRole.VIEWER);
            } else {
                updatedSnakes.add(snake);
            }
        }

        currentState = new GameState(currentState.getStateOrder(), updatedSnakes, currentState.getFoods(), currentState.getPlayers());
        if (playerId == deputyId) {
            selectNewDeputy();
        }

        if (stateListener != null) {
            stateListener.onGameStateUpdated(currentState);
            stateListener.onPlayerListUpdated(currentState.getPlayers());
        }
    }

    private void selectNewDeputy() {
        for (GamePlayer player : currentState.getPlayers()) {
            if (player.getRole() == SnakesProto.NodeRole.NORMAL) {
                deputyId = player.getId();
                InetSocketAddress address = playerAddresses.get(deputyId);
                sendRoleChange(deputyId, SnakesProto.NodeRole.DEPUTY, address.getAddress(), address.getPort());
            }
        }
    }

    private void updatePlayerRole(int playerId, SnakesProto.NodeRole newRole) {
        if (currentState == null) {
            this.role = newRole;
            return;
        }

        List<GamePlayer> players = currentState.getPlayers();
        List<GamePlayer> updatedPlayers = new ArrayList<>();

        for (GamePlayer player : players) {
            if (player.getId() == playerId) {
                updatedPlayers.add(player.withRole(newRole));
            } else {
                updatedPlayers.add(player);
            }
        }

        if (this.playerId == playerId) {
            this.role = newRole;
        }

        currentState = new GameState(currentState.getStateOrder(), currentState.getSnakes(), currentState.getFoods(), updatedPlayers);
    }

    private void updateFood() {
        if (currentState == null || config == null) {
            return;
        }

        Set<Coord> foods = new HashSet<>(currentState.getFoods());
        List<Snake> snakes = currentState.getSnakes();

        int aliveSnakes = 0;
        for (Snake snake : snakes) {
            if (snake.getState() == SnakesProto.GameState.Snake.SnakeState.ALIVE) {
                aliveSnakes++;
            }
        }

        int requiredFood = config.getFoodStatic() + aliveSnakes;

        System.out.println("=== UPDATING FOOD ===");
        System.out.println("Current food: " + foods.size());
        System.out.println("Alive snakes: " + aliveSnakes);
        System.out.println("Required food: " + requiredFood + " (static: " + config.getFoodStatic() + " + snakes: " + aliveSnakes + ")");

        int addedCount = 0;
        while (foods.size() < requiredFood) {
            Coord newFood = findFreeCellForFood(snakes, foods);
            if (newFood != null) {
                foods.add(newFood);
                addedCount++;
                System.out.println("  Added food at: " + newFood);
            } else {
                System.err.println("  Could not find free cell for new food");
                break;
            }

            if (addedCount > 100) {
                System.err.println("  Too many attempts to add food, stopping");
                break;
            }
        }

        System.out.println("Added " + addedCount + " new food items");
        System.out.println("Total food now: " + foods.size());
        System.out.println("=== END UPDATING FOOD ===");

        currentState = new GameState(currentState.getStateOrder(), currentState.getSnakes(), foods, currentState.getPlayers());
    }

    private Coord findFreeCellForFood(List<Snake> snakes, Set<Coord> existingFoods) {
        if (config == null) return null;

        int width = config.getWidth();
        int height = config.getHeight();

        Set<Coord> occupiedCells = new HashSet<>();

        for (Snake snake : snakes) {
            List<Coord> segments = snake.getAllSegments(width, height);
            occupiedCells.addAll(segments);
        }

        occupiedCells.addAll(existingFoods);

        if (occupiedCells.size() >= width * height) {
            System.err.println("  No free cells on the field!");
            return null;
        }

        int maxAttempts = width * height * 2;
        for (int i = 0; i < maxAttempts; i++) {
            int x = random.nextInt(width);
            int y = random.nextInt(height);
            Coord coord = new Coord(x, y);

            if (!occupiedCells.contains(coord)) {
                return coord;
            }
        }
        return null;
    }

    private void increasePlayerScore(int playerId, int increment) {
        List<GamePlayer> players = currentState.getPlayers();
        List<GamePlayer> updatedPlayers = new ArrayList<>();

        for (GamePlayer player : players) {
            if (player.getId() == playerId) {
                updatedPlayers.add(player.withScore(player.getScore() + increment));
            } else {
                updatedPlayers.add(player);
            }
        }

        currentState = new GameState(currentState.getStateOrder(), currentState.getSnakes(), currentState.getFoods(), updatedPlayers);
    }


    private void broadcastGameState() {
        if (role != SnakesProto.NodeRole.MASTER || networkManager == null) {
            return;
        }

        SnakesProto.GameMessage stateMsg = networkManager.createStateMsg(currentState.toProto(), playerId);

        for (Map.Entry<Integer, InetSocketAddress> entry : playerAddresses.entrySet()) {
            InetSocketAddress address = entry.getValue();
            networkManager.sendUnicast(stateMsg, address.getAddress(), address.getPort());
        }

        System.out.println("Broadcasted game state #" + currentState.getStateOrder() + " to " + playerAddresses.size() + " players");
    }

    private void startAnnouncements() {
        if (role != SnakesProto.NodeRole.MASTER) {
            return;
        }

        if (announcementFuture != null) {
            announcementFuture.cancel(true);
        }

        announcementFuture = gameLoopExecutor.scheduleAtFixedRate(() -> {
            sendGameAnnouncement();
        }, 0, 1, TimeUnit.SECONDS);
    }


    private void sendGameAnnouncement() {
        if (networkManager == null) {
            return;
        }

        SnakesProto.GameAnnouncement announcement = SnakesProto.GameAnnouncement.newBuilder().setGameName(gameName).setConfig(config.toProto()).setPlayers(SnakesProto.GamePlayers.newBuilder().addAllPlayers(getPlayersAsProto())).setCanJoin(true).build();

        List<SnakesProto.GameAnnouncement> games = new ArrayList<>();
        games.add(announcement);

        SnakesProto.GameMessage announcementMsg = networkManager.createAnnouncement(games);
        networkManager.sendMulticast(announcementMsg);
    }


    private List<SnakesProto.GamePlayer> getPlayersAsProto() {
        List<SnakesProto.GamePlayer> protoPlayers = new ArrayList<>();
        for (GamePlayer player : currentState.getPlayers()) {
            protoPlayers.add(player.toProto());
        }
        return protoPlayers;
    }

    private Integer findPlayerIdByAddress(InetSocketAddress address) {
        if (address == null) return null;

        for (Map.Entry<Integer, InetSocketAddress> entry : playerAddresses.entrySet()) {
            if (entry.getValue().equals(address)) {
                return entry.getKey();
            }
        }
        return null;
    }

    private void handleSteer(SnakesProto.GameMessage message) {
        if (role != SnakesProto.NodeRole.MASTER) {
            return;
        }
        System.out.println("Received Steer message" + message.getSenderId());

        int senderId = message.getSenderId();
        SnakesProto.Direction direction = message.getSteer().getDirection();
        long msgSeq = message.getMsgSeq();
        PendingSteer existing = pendingSteers.get(senderId);
        if (existing == null || msgSeq > existing.msgSeq) {
            pendingSteers.put(senderId, new PendingSteer(direction, msgSeq));
        }
        System.out.println("[DEBUG sendSteerCommand] START: " +
                "role=" + message.getSteer().toString() +
                ", playerId=" + message.getSenderId() +
                ", direction=" + message.getSteer().getDirection());
        System.out.println("steeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeer");
    }

    private void handleState(SnakesProto.GameMessage message) {
        if (role == SnakesProto.NodeRole.MASTER) {
            return;
        }

        SnakesProto.GameState stateProto = message.getState().getState();
        GameState newState = new GameState(stateProto);

        if (currentState == null || newState.getStateOrder() > currentState.getStateOrder()) {
            currentState = newState;

            if (stateListener != null) {
                SwingUtilities.invokeLater(() -> {
                    stateListener.onGameStateUpdated(currentState);
                    stateListener.onPlayerListUpdated(currentState.getPlayers());
                });
            }

            if (masterAddress != null && masterPort > 0) {
                networkManager.sendAck(message.getMsgSeq(), playerId, message.getSenderId(), masterAddress, masterPort);
            }
        }
    }


    public record AnnouncedGame(SnakesProto.GameAnnouncement announcement, InetAddress address, int port) {
    }

    private void handleAnnouncement(SnakesProto.GameMessage message, InetAddress senderAddress, int senderPort) {
        List<SnakesProto.GameAnnouncement> announcements = message.getAnnouncement().getGamesList();

        List<AnnouncedGame> gamesWithSource = new ArrayList<>();
        for (SnakesProto.GameAnnouncement ann : announcements) {
            gamesWithSource.add(new AnnouncedGame(ann, senderAddress, senderPort));
        }

        if (gameListListener != null) {
            gameListListener.onGameListUpdated(gamesWithSource);
        }
    }

    private void handleRoleChange(SnakesProto.GameMessage message) {
        SnakesProto.GameMessage.RoleChangeMsg roleChange = message.getRoleChange();

        if (roleChange.hasReceiverRole()) {
            SnakesProto.NodeRole newRole = roleChange.getReceiverRole();
            this.role = newRole;
            System.out.println("Role changed to: " + role);

            if (currentState != null) {
                updatePlayerRole(playerId, newRole);
            }

            if (newRole == SnakesProto.NodeRole.MASTER) {
                masterAddress = null;
                masterPort = 0;

                if (gameLoopFuture != null) {
                    gameLoopFuture.cancel(true);
                    gameLoopFuture = null;
                }
                startGameLoop();
                startAnnouncements();

                System.out.println("I am now the MASTER!");
            }
        }
    }

    private void handleError(SnakesProto.GameMessage message) {
        String errorMsg = message.getError().getErrorMessage();
        if (stateListener != null) {
            stateListener.onErrorMessage(errorMsg);
        }
    }


    private void handlePing(SnakesProto.GameMessage message, InetAddress senderAddress, int senderPort) {
        networkManager.sendAck(message.getMsgSeq(), playerId, message.getSenderId(), senderAddress, senderPort);
    }


    private void handleAck(SnakesProto.GameMessage message) {
        System.out.println("ACK received for msgSeq: " + message.getMsgSeq());
        if (message.getMsgSeq() == lastJoinMsgSeq && message.getReceiverId() > 0) {
            this.playerId = message.getReceiverId();
            System.out.println("Assigned playerId: " + this.playerId);
        }
    }

    public void sendSteerCommand(SnakesProto.Direction direction) {
        System.out.println("[DEBUG sendSteerCommand] START: role=" + role +
                ", playerId=" + playerId + ", direction=" + direction);

        if (networkManager == null) {
            System.out.println("[ERROR] networkManager is null");
            return;
        }

        if (role == SnakesProto.NodeRole.MASTER) {
            long seq = System.nanoTime();
            PendingSteer existing = pendingSteers.get(playerId);
            if (existing == null || seq > existing.msgSeq) {
                pendingSteers.put(playerId, new PendingSteer(direction, seq));
            }
            return;
        }

        if (role == SnakesProto.NodeRole.DEPUTY || role == SnakesProto.NodeRole.NORMAL) {
            GamePlayer master = findMasterPlayer();
            if (master == null) {
                System.out.println("[ERROR] Master player not found, but we are " + role);

                if (role == SnakesProto.NodeRole.DEPUTY) {
                    System.out.println("[INFO] DEPUTY cannot find MASTER, attempting to become MASTER...");
                    becomeMaster();
                    long seq = System.nanoTime();
                    PendingSteer existing = pendingSteers.get(playerId);
                    if (existing == null || seq > existing.msgSeq) {
                        pendingSteers.put(playerId, new PendingSteer(direction, seq));
                    }
                }
                return;
            }

            if (masterAddress == null) {
                System.out.println("[ERROR] masterAddress is null");
                return;
            }

            try {
                SnakesProto.GameMessage steerMsg = networkManager.createSteerMsg(direction, playerId);
                networkManager.sendUnicast(steerMsg, masterAddress, masterPort);

            } catch (Exception e) {
                System.out.println("[ERROR] Failed to send steer: " + e.getMessage());
                e.printStackTrace();
            }
        } else {
            System.out.println("[ERROR] Cannot steer: role=" + role);
        }
    }
    private GamePlayer findMasterPlayer() {
        if (currentState == null) {
            return null;
        }

        for (GamePlayer player : currentState.getPlayers()) {
            if (player.isMaster()) {
                return player;
            }
        }

        return null;
    }

    private int generatePlayerId() {
        int maxId = 0;
        for (GamePlayer player : currentState.getPlayers()) {
            if (player.getId() > maxId) {
                maxId = player.getId();
            }
        }
        return maxId + 1;
    }


    private void sendRoleChange(int receiverId, SnakesProto.NodeRole newRole, InetAddress address, int port) {
        SnakesProto.GameMessage roleChangeMsg = SnakesProto.GameMessage.newBuilder().setMsgSeq(System.currentTimeMillis()).setSenderId(playerId).setReceiverId(receiverId).setRoleChange(SnakesProto.GameMessage.RoleChangeMsg.newBuilder().setReceiverRole(newRole).build()).build();

        networkManager.sendUnicast(roleChangeMsg, address, port);
    }

    private InetAddress getSenderAddress(int playerId) {
        InetSocketAddress address = playerAddresses.get(playerId);
        return address != null ? address.getAddress() : null;
    }

    private int getSenderPort(int playerId) {
        InetSocketAddress address = playerAddresses.get(playerId);
        return address != null ? address.getPort() : 0;
    }


    public void stopGame() {
        if (gameLoopFuture != null) {
            gameLoopFuture.cancel(true);
        }

        if (announcementFuture != null) {
            announcementFuture.cancel(true);
        }

        if (gameLoopExecutor != null) {
            gameLoopExecutor.shutdown();
        }

        if (networkManager != null) {
            networkManager.stop();
        }
    }

    public GameState getCurrentState() {
        return currentState;
    }

    public GameConfig getConfig() {
        return config;
    }

    public String getGameName() {
        return gameName;
    }

    public int getPlayerId() {
        return playerId;
    }

    public SnakesProto.NodeRole getRole() {
        return role;
    }

    public int getLastStateOrder() {
        return currentState != null ? currentState.getStateOrder() : -1;
    }

    public void setStateListener(GameStateListener listener) {
        this.stateListener = listener;
    }

    public void setGameListListener(GameListListener listener) {
        this.gameListListener = listener;
    }

    public boolean isMaster() {
        return role == SnakesProto.NodeRole.MASTER;
    }

    public boolean isNormal() {
        return role == SnakesProto.NodeRole.NORMAL;
    }

    public boolean isViewer() {
        return role == SnakesProto.NodeRole.VIEWER;
    }
}