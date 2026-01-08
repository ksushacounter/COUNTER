package ru.nsu.garkusha.game;

import ru.nsu.garkusha.proto.SnakesProto;

public class GamePlayer {
    private final String name;
    private final int id;
    private final String ipAddress;
    private final int port;
    private final SnakesProto.NodeRole role;
    private final SnakesProto.PlayerType type;
    private final int score;

    public GamePlayer(String name, int id, SnakesProto.NodeRole role, int score) {
        this(name, id, null, 0, role, SnakesProto.PlayerType.HUMAN, score);
    }

    public GamePlayer(String name, int id, String ipAddress, int port,
                      SnakesProto.NodeRole role, SnakesProto.PlayerType type, int score) {
        this.name = name;
        this.id = id;
        this.ipAddress = ipAddress;
        this.port = port;
        this.role = role;
        this.type = type;
        this.score = score;
    }

    public GamePlayer(SnakesProto.GamePlayer playerProto) {
        this.name = playerProto.getName();
        this.id = playerProto.getId();
        this.ipAddress = playerProto.hasIpAddress() ? playerProto.getIpAddress() : null;
        this.port = playerProto.hasPort() ? playerProto.getPort() : 0;
        this.role = playerProto.getRole();
        this.type = playerProto.getType();
        this.score = playerProto.getScore();
    }

    public SnakesProto.GamePlayer toProto() {
        SnakesProto.GamePlayer.Builder builder = SnakesProto.GamePlayer.newBuilder()
                .setName(name)
                .setId(id)
                .setRole(role)
                .setType(type)
                .setScore(score);

        if (ipAddress != null && port > 0) {
            builder.setIpAddress(ipAddress).setPort(port);
        }

        return builder.build();
    }

    public GamePlayer withScore(int newScore) {
        return new GamePlayer(name, id, ipAddress, port, role, type, newScore);
    }

    public GamePlayer withRole(SnakesProto.NodeRole newRole) {
        return new GamePlayer(name, id, ipAddress, port, newRole, type, score);
    }

    public void setRole(SnakesProto.NodeRole newRole) {}
    public String getName() { return name; }
    public int getId() { return id; }
    public String getIpAddress() { return ipAddress; }
    public int getPort() { return port; }
    public SnakesProto.NodeRole getRole() { return role; }
    public SnakesProto.PlayerType getType() { return type; }
    public int getScore() { return score; }

    public boolean isMaster() { return role == SnakesProto.NodeRole.MASTER; }
    public boolean isDeputy() { return role == SnakesProto.NodeRole.DEPUTY; }
    public boolean isViewer() { return role == SnakesProto.NodeRole.VIEWER; }

    @Override
    public String toString() {
        return String.format("%s (ID: %d, Score: %d, Role: %s)",
                name, id, score, role);
    }
}