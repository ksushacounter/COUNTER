package ru.nsu.garkusha.ui;

import ru.nsu.garkusha.game.*;
import ru.nsu.garkusha.game.Coord;
import ru.nsu.garkusha.game.GameState;
import ru.nsu.garkusha.game.Snake;
import ru.nsu.garkusha.proto.SnakesProto;
import javax.swing.*;
import java.awt.*;

public class GamePanel extends JPanel {
    private GameLogic gameLogic;
    private GameState currentState;
    private int cellSize = 20;

    private final Color[] snakeColors = {
            new Color(66, 133, 244),
            new Color(219, 68, 55),
            new Color(244, 180, 0),
            new Color(15, 157, 88),
            new Color(171, 71, 188),
            new Color(0, 172, 193),
            new Color(255, 112, 67),
            new Color(121, 85, 72)
    };

    private final Color foodColor = new Color(255, 87, 34);
    private final Color zombieColor = new Color(128, 128, 128);
    private final Color backgroundColor = new Color(240, 240, 240);
    private final Color gridColor = new Color(220, 220, 220);

    public GamePanel(GameLogic gameLogic) {
        this.gameLogic = gameLogic;
        setBackground(backgroundColor);
        setPreferredSize(calculatePreferredSize());
    }

    private Dimension calculatePreferredSize() {
        if (gameLogic.getConfig() == null) {
            return new Dimension(800, 600);
        }

        int width = gameLogic.getConfig().getWidth() * cellSize;
        int height = gameLogic.getConfig().getHeight() * cellSize;

        return new Dimension(width, height);
    }

    public void updateGameState(GameState state) {
        this.currentState = state;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        if (currentState == null || gameLogic.getConfig() == null) {
            drawWaitingMessage(g);
            return;
        }

        Graphics2D g2d = (Graphics2D) g;
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                RenderingHints.VALUE_ANTIALIAS_ON);

        drawGrid(g2d);
        drawFood(g2d);
        drawSnakes(g2d);
        drawFieldInfo(g2d);
    }

    private void drawGrid(Graphics2D g2d) {
        int width = gameLogic.getConfig().getWidth();
        int height = gameLogic.getConfig().getHeight();

        g2d.setColor(gridColor);

        for (int x = 0; x <= width; x++) {
            int pixelX = x * cellSize;
            g2d.drawLine(pixelX, 0, pixelX, height * cellSize);
        }

        for (int y = 0; y <= height; y++) {
            int pixelY = y * cellSize;
            g2d.drawLine(0, pixelY, width * cellSize, pixelY);
        }
    }


    private void drawFood(Graphics2D g2d) {
        g2d.setColor(foodColor);

        for (Coord food : currentState.getFoods()) {
            int x = food.getX() * cellSize;
            int y = food.getY() * cellSize;

            g2d.fillOval(x + 2, y + 2, cellSize - 4, cellSize - 4);

            g2d.setColor(foodColor.darker());
            g2d.drawOval(x + 2, y + 2, cellSize - 4, cellSize - 4);
            g2d.setColor(foodColor);
        }
    }


    private void drawSnakes(Graphics2D g2d) {
        int width = gameLogic.getConfig().getWidth();
        int height = gameLogic.getConfig().getHeight();

        for (Snake snake : currentState.getSnakes()) {
            Color snakeColor = snakeColors[snake.getPlayerId() % snakeColors.length];

            if (snake.getState() == SnakesProto.GameState.Snake.SnakeState.ZOMBIE) {
                snakeColor = zombieColor;
            }

            java.util.List<Coord> segments = snake.getAllSegments(width, height);

            g2d.setColor(snakeColor);
            for (int i = 0; i < segments.size(); i++) {
                Coord segment = segments.get(i);
                int x = segment.getX() * cellSize;
                int y = segment.getY() * cellSize;

                if (i == 0) {
                    drawSnakeHead(g2d, x, y, snake.getHeadDirection(), snakeColor);
                } else if (i == segments.size() - 1) {
                    drawSnakeTail(g2d, x, y, segments.get(i-1), segment, snakeColor);
                } else {
                    g2d.fillRect(x + 2, y + 2, cellSize - 4, cellSize - 4);

                    g2d.setColor(snakeColor.darker());
                    g2d.drawRect(x + 2, y + 2, cellSize - 4, cellSize - 4);
                    g2d.setColor(snakeColor);
                }
            }

            if (!segments.isEmpty()) {
                Coord head = segments.get(0);
                g2d.setColor(Color.BLACK);
                g2d.setFont(new Font("Arial", Font.BOLD, 10));
                String idText = String.valueOf(snake.getPlayerId());
                int textX = head.getX() * cellSize + cellSize/2 - 3;
                int textY = head.getY() * cellSize - 5;
                g2d.drawString(idText, textX, textY);
            }
        }
    }


    private void drawSnakeHead(Graphics2D g2d, int x, int y,
                               SnakesProto.Direction direction, Color color) {
        g2d.setColor(color);
        g2d.fillRect(x + 2, y + 2, cellSize - 4, cellSize - 4);

        g2d.setColor(color.darker());
        g2d.drawRect(x + 2, y + 2, cellSize - 4, cellSize - 4);

        g2d.setColor(Color.WHITE);
        int eyeSize = cellSize / 4;

        switch (direction) {
            case UP:
                g2d.fillOval(x + cellSize/4, y + cellSize/4, eyeSize, eyeSize);
                g2d.fillOval(x + 3*cellSize/4 - eyeSize, y + cellSize/4, eyeSize, eyeSize);
                break;
            case DOWN:
                g2d.fillOval(x + cellSize/4, y + 3*cellSize/4 - eyeSize, eyeSize, eyeSize);
                g2d.fillOval(x + 3*cellSize/4 - eyeSize, y + 3*cellSize/4 - eyeSize, eyeSize, eyeSize);
                break;
            case LEFT:
                g2d.fillOval(x + cellSize/4, y + cellSize/4, eyeSize, eyeSize);
                g2d.fillOval(x + cellSize/4, y + 3*cellSize/4 - eyeSize, eyeSize, eyeSize);
                break;
            case RIGHT:
                g2d.fillOval(x + 3*cellSize/4 - eyeSize, y + cellSize/4, eyeSize, eyeSize);
                g2d.fillOval(x + 3*cellSize/4 - eyeSize, y + 3*cellSize/4 - eyeSize, eyeSize, eyeSize);
                break;
        }

        g2d.setColor(Color.BLACK);
        int pupilSize = eyeSize / 2;

        switch (direction) {
            case UP:
                g2d.fillOval(x + cellSize/4 + pupilSize/2, y + cellSize/4, pupilSize, pupilSize);
                g2d.fillOval(x + 3*cellSize/4 - eyeSize + pupilSize/2, y + cellSize/4, pupilSize, pupilSize);
                break;
            case DOWN:
                g2d.fillOval(x + cellSize/4 + pupilSize/2, y + 3*cellSize/4 - eyeSize, pupilSize, pupilSize);
                g2d.fillOval(x + 3*cellSize/4 - eyeSize + pupilSize/2, y + 3*cellSize/4 - eyeSize, pupilSize, pupilSize);
                break;
            case LEFT:
                g2d.fillOval(x + cellSize/4, y + cellSize/4 + pupilSize/2, pupilSize, pupilSize);
                g2d.fillOval(x + cellSize/4, y + 3*cellSize/4 - eyeSize + pupilSize/2, pupilSize, pupilSize);
                break;
            case RIGHT:
                g2d.fillOval(x + 3*cellSize/4 - eyeSize, y + cellSize/4 + pupilSize/2, pupilSize, pupilSize);
                g2d.fillOval(x + 3*cellSize/4 - eyeSize, y + 3*cellSize/4 - eyeSize + pupilSize/2, pupilSize, pupilSize);
                break;
        }
    }

    private void drawSnakeTail(Graphics2D g2d, int x, int y,
                               Coord prevSegment, Coord tail, Color color) {
        int dx = tail.getX() - prevSegment.getX();
        int dy = tail.getY() - prevSegment.getY();

        if (dx > 1) dx = -1;
        if (dx < -1) dx = 1;
        if (dy > 1) dy = -1;
        if (dy < -1) dy = 1;

        g2d.setColor(color);

        if (dx == 1) {
            int[] xPoints = {x + cellSize - 2, x + 2, x + 2};
            int[] yPoints = {y + cellSize/2, y + 2, y + cellSize - 2};
            g2d.fillPolygon(xPoints, yPoints, 3);
        } else if (dx == -1) {
            int[] xPoints = {x + 2, x + cellSize - 2, x + cellSize - 2};
            int[] yPoints = {y + cellSize/2, y + 2, y + cellSize - 2};
            g2d.fillPolygon(xPoints, yPoints, 3);
        } else if (dy == 1) {
            int[] xPoints = {x + 2, x + cellSize - 2, x + cellSize/2};
            int[] yPoints = {y + 2, y + 2, y + cellSize - 2};
            g2d.fillPolygon(xPoints, yPoints, 3);
        } else if (dy == -1) {
            int[] xPoints = {x + 2, x + cellSize - 2, x + cellSize/2};
            int[] yPoints = {y + cellSize - 2, y + cellSize - 2, y + 2};
            g2d.fillPolygon(xPoints, yPoints, 3);
        } else {
            g2d.fillRect(x + 2, y + 2, cellSize - 4, cellSize - 4);
        }

        g2d.setColor(color.darker());
        g2d.drawRect(x + 2, y + 2, cellSize - 4, cellSize - 4);
    }

    private void drawFieldInfo(Graphics2D g2d) {
        g2d.setColor(Color.BLACK);
        g2d.setFont(new Font("Arial", Font.PLAIN, 12));

        String info = String.format("Turn: %d | Food: %d | Snakes: %d",
                currentState.getStateOrder(),
                currentState.getFoods().size(),
                currentState.getSnakes().size());

        g2d.drawString(info, 10, 20);

        String roleInfo = "Your role: " + getRoleString(gameLogic.getRole());
        if (gameLogic.getPlayerId() > 0) {
            roleInfo += " (ID: " + gameLogic.getPlayerId() + ")";
        }

        g2d.drawString(roleInfo, 10, 40);
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


    private void drawWaitingMessage(Graphics g) {
        Graphics2D g2d = (Graphics2D) g;

        g2d.setColor(Color.GRAY);
        g2d.setFont(new Font("Arial", Font.BOLD, 24));

        String message = "Waiting for game state...";
        FontMetrics fm = g2d.getFontMetrics();
        int x = (getWidth() - fm.stringWidth(message)) / 2;
        int y = getHeight() / 2;

        g2d.drawString(message, x, y);
    }


    public void setCellSize(int cellSize) {
        this.cellSize = Math.max(5, Math.min(50, cellSize));
        setPreferredSize(calculatePreferredSize());
        revalidate();
        repaint();
    }

    public int getCellSize() {
        return cellSize;
    }
}