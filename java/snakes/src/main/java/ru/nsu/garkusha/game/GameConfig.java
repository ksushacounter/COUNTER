package ru.nsu.garkusha.game;

import ru.nsu.garkusha.proto.SnakesProto;

public class GameConfig {
    private final int width;
    private final int height;
    private final int foodStatic;
    private final int stateDelayMs;

    public GameConfig(int width, int height, int foodStatic, int stateDelayMs) {
        if (width < 10 || width > 100) {
            throw new IllegalArgumentException("Width must be between 10 and 100");
        }
        if (height < 10 || height > 100) {
            throw new IllegalArgumentException("Height must be between 10 and 100");
        }
        if (foodStatic < 0 || foodStatic > 100) {
            throw new IllegalArgumentException("Food static must be between 0 and 100");
        }
        if (stateDelayMs < 100 || stateDelayMs > 3000) {
            throw new IllegalArgumentException("State delay must be between 100 and 3000 ms");
        }

        this.width = width;
        this.height = height;
        this.foodStatic = foodStatic;
        this.stateDelayMs = stateDelayMs;
    }

    public GameConfig(SnakesProto.GameConfig config) {
        this.width = config.getWidth();
        this.height = config.getHeight();
        this.foodStatic = config.getFoodStatic();
        this.stateDelayMs = config.getStateDelayMs();
    }

    public SnakesProto.GameConfig toProto() {
        return SnakesProto.GameConfig.newBuilder()
                .setWidth(width)
                .setHeight(height)
                .setFoodStatic(foodStatic)
                .setStateDelayMs(stateDelayMs)
                .build();
    }

    public int getWidth() { return width; }
    public int getHeight() { return height; }
    public int getFoodStatic() { return foodStatic; }
    public int getStateDelayMs() { return stateDelayMs; }

    @Override
    public String toString() {
        return String.format("Field: %dx%d, Food: %d, Delay: %dms",
                width, height, foodStatic, stateDelayMs);
    }
}