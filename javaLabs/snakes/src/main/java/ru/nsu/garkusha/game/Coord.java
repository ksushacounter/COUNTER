package ru.nsu.garkusha.game;

import ru.nsu.garkusha.proto.SnakesProto;

public class Coord {
    private final int x;
    private final int y;

    public Coord(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public Coord(SnakesProto.GameState.Coord coord) {
        this(coord.getX(), coord.getY());
    }

    public SnakesProto.GameState.Coord toProto() {
        return SnakesProto.GameState.Coord.newBuilder()
                .setX(x)
                .setY(y)
                .build();
    }

    public Coord normalize(int width, int height) {
        int newX = x % width;
        int newY = y % height;
        if (newX < 0) newX += width;
        if (newY < 0) newY += height;
        return new Coord(newX, newY);
    }

    public Coord move(SnakesProto.Direction direction) {
        switch (direction) {
            case UP:
                return new Coord(x, y - 1);
            case DOWN:
                return new Coord(x, y + 1);
            case LEFT:
                return new Coord(x - 1, y);
            case RIGHT:
                return new Coord(x + 1, y);
            default:
                return this;
        }
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Coord other = (Coord) obj;
        return x == other.x && y == other.y;
    }

    @Override
    public int hashCode() {
        return 31 * x + y;
    }

    public int getX() { return x; }
    public int getY() { return y; }

    @Override
    public String toString() {
        return String.format("(%d, %d)", x, y);
    }
}