package ru.nsu.garkusha.game;

import ru.nsu.garkusha.proto.SnakesProto;
import java.util.*;

public class GameState {
    private final int stateOrder;
    private final List<Snake> snakes;
    private final Set<Coord> foods;
    private final List<GamePlayer> players;

    public GameState(int stateOrder, List<Snake> snakes,
                     Set<Coord> foods, List<GamePlayer> players) {
        this.stateOrder = stateOrder;
        this.snakes = new ArrayList<>(snakes);
        this.foods = new HashSet<>(foods);
        this.players = new ArrayList<>(players);
    }

    public GameState(SnakesProto.GameState stateProto) {
        this.stateOrder = stateProto.getStateOrder();

        this.snakes = new ArrayList<>();
        for (SnakesProto.GameState.Snake snakeProto : stateProto.getSnakesList()) {
            snakes.add(new Snake(snakeProto));
        }

        this.foods = new HashSet<>();
        for (SnakesProto.GameState.Coord foodCoord : stateProto.getFoodsList()) {
            foods.add(new Coord(foodCoord));
        }

        this.players = new ArrayList<>();
        for (SnakesProto.GamePlayer playerProto : stateProto.getPlayers().getPlayersList()) {
            players.add(new GamePlayer(playerProto));
        }
    }

    public SnakesProto.GameState toProto() {
        SnakesProto.GameState.Builder builder = SnakesProto.GameState.newBuilder()
                .setStateOrder(stateOrder);

        for (Snake snake : snakes) {
            builder.addSnakes(snake.toProto());
        }

        for (Coord food : foods) {
            builder.addFoods(food.toProto());
        }

        SnakesProto.GamePlayers.Builder playersBuilder = SnakesProto.GamePlayers.newBuilder();
        for (GamePlayer player : players) {
            playersBuilder.addPlayers(player.toProto());
        }
        builder.setPlayers(playersBuilder.build());

        return builder.build();
    }

    public Snake getSnakeByPlayerId(int playerId) {
        for (Snake snake : snakes) {
            if (snake.getPlayerId() == playerId) {
                return snake;
            }
        }
        return null;
    }

    public GamePlayer getPlayerById(int playerId) {
        for (GamePlayer player : players) {
            if (player.getId() == playerId) {
                return player;
            }
        }
        return null;
    }

    public boolean isCellOccupied(Coord coord, int width, int height) {
        for (Snake snake : snakes) {
            if (snake.contains(coord.normalize(width, height), width, height)) {
                return true;
            }
        }
        return false;
    }

    public boolean isFoodAt(Coord coord) {
        return foods.contains(coord);
    }

    public void addFood(Coord coord) {
        foods.add(coord);
    }

    public void removeFood(Coord coord) {
        foods.remove(coord);
    }

    public int getStateOrder() { return stateOrder; }
    public List<Snake> getSnakes() { return new ArrayList<>(snakes); }
    public Set<Coord> getFoods() { return new HashSet<>(foods); }
    public List<GamePlayer> getPlayers() { return new ArrayList<>(players); }

    @Override
    public String toString() {
        return String.format("GameState[order=%d, snakes=%d, food=%d, players=%d]",
                stateOrder, snakes.size(), foods.size(), players.size());
    }
}