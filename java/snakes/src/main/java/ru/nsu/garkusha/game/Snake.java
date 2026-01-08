package ru.nsu.garkusha.game;

import ru.nsu.garkusha.proto.SnakesProto;

import java.util.*;

public class Snake {
    private int playerId;
    private List<Coord> points;
    private SnakesProto.GameState.Snake.SnakeState state;
    private SnakesProto.Direction headDirection;

    public Snake(int playerId, List<Coord> points,
                 SnakesProto.GameState.Snake.SnakeState state,
                 SnakesProto.Direction headDirection) {
        this.playerId = playerId;
        this.points = new ArrayList<>(points);
        this.state = state;
        this.headDirection = headDirection;
    }

    public Snake(SnakesProto.GameState.Snake snakeProto) {
        this.playerId = snakeProto.getPlayerId();
        this.state = snakeProto.getState();
        this.headDirection = snakeProto.getHeadDirection();

        this.points = new ArrayList<>();
        for (SnakesProto.GameState.Coord coord : snakeProto.getPointsList()) {
            points.add(new Coord(coord));
        }
    }

    public SnakesProto.GameState.Snake toProto() {
        SnakesProto.GameState.Snake.Builder builder = SnakesProto.GameState.Snake.newBuilder()
                .setPlayerId(playerId)
                .setState(state)
                .setHeadDirection(headDirection);

        for (Coord point : points) {
            builder.addPoints(point.toProto());
        }

        return builder.build();
    }

    public List<Coord> getAllSegments(int width, int height) {
        List<Coord> segments = new ArrayList<>();

        if (points == null || points.isEmpty()) {
            return segments;
        }

        Coord current = points.get(0).normalize(width, height);
        segments.add(current);

        for (int i = 1; i < points.size(); i++) {
            Coord relative = points.get(i);
            current = new Coord(
                    current.getX() + relative.getX(),
                    current.getY() + relative.getY()
            ).normalize(width, height);
            segments.add(current);
        }

        return segments;
    }


    public Coord getHead(int width, int height) {
        if (points == null || points.isEmpty()) {
            System.err.println("Warning: Snake has no points! Player ID: " + playerId);
            return new Coord(0, 0).normalize(width, height);
        }
        return points.get(0).normalize(width, height);
    }

    public boolean contains(Coord coord, int width, int height) {
        List<Coord> segments = getAllSegments(width, height);
        boolean contains = segments.contains(coord.normalize(width, height));

        if (contains) {
            System.out.println("Snake contains coord " + coord +
                    ", segments: " + segments.size() +
                    ", head: " + getHead(width, height));
        }

        return contains;
    }

    public Coord moveSimple(boolean eatFood, int width, int height) {
        if (points == null || points.isEmpty()) {
            return null;
        }

        List<Coord> segments = getAllSegments(width, height);

        Coord newHead = segments.get(0).move(headDirection).normalize(width, height);

        if (eatFood) {
            segments.add(0, newHead);
        } else {
            Coord oldTail = segments.remove(segments.size() - 1);
            segments.add(0, newHead);

            updatePointsFromSegments(segments);
            return oldTail;
        }

        updatePointsFromSegments(segments);
        return null;
    }


    private void updatePointsFromSegments(List<Coord> segments) {
        points.clear();

        if (segments.isEmpty()) return;

        points.add(segments.get(0));

        for (int i = 1; i < segments.size(); i++) {
            Coord prev = segments.get(i - 1);
            Coord current = segments.get(i);
            Coord offset = new Coord(
                    current.getX() - prev.getX(),
                    current.getY() - prev.getY()
            );
            points.add(offset);
        }
    }

    public boolean setDirection(SnakesProto.Direction newDirection, int width, int height) {
        if ((headDirection == SnakesProto.Direction.UP && newDirection == SnakesProto.Direction.DOWN) ||
                (headDirection == SnakesProto.Direction.DOWN && newDirection == SnakesProto.Direction.UP) ||
                (headDirection == SnakesProto.Direction.LEFT && newDirection == SnakesProto.Direction.RIGHT) ||
                (headDirection == SnakesProto.Direction.RIGHT && newDirection == SnakesProto.Direction.LEFT)) {
            return false;
        }

        Coord nextHead = getHead(width, height).move(newDirection).normalize(width, height);
        List<Coord> segments = getAllSegments(width, height);
        if (segments.size() > 1 && nextHead.equals(segments.get(1))) {
            return false;
        }
        System.out.println("3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333");

        this.headDirection = newDirection;
        return true;
    }

    public boolean isSelfCollision(int width, int height) {
        List<Coord> segments = getAllSegments(width, height);
        Coord head = segments.get(0);

        for (int i = 1; i < segments.size(); i++) {
            if (head.equals(segments.get(i))) {
                return true;
            }
        }
        return false;
    }

    public int getPlayerId() {
        return playerId;
    }

    public List<Coord> getPoints() {
        return new ArrayList<>(points);
    }

    public SnakesProto.GameState.Snake.SnakeState getState() {
        return state;
    }

    public SnakesProto.Direction getHeadDirection() {
        return headDirection;
    }

    public void setState(SnakesProto.GameState.Snake.SnakeState state) {
        this.state = state;
    }

    public int getLength() {
        if (points == null) return 0;
        return points.size();
    }

    @Override
    public String toString() {
        return String.format("Snake[player=%d, points=%d, segments=%d, dir=%s]",
                playerId,
                points != null ? points.size() : 0,
                points != null && !points.isEmpty() ?
                        getAllSegments(100, 100).size() : 0,
                headDirection);
    }
}