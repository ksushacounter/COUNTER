package org.example.model;

public class Collision {

    public static boolean checkCollision(GameObject player, GameObject tire) {
        int playerLeft = player.getX();
        int playerRight = player.getX() + player.getWidth();
        int playerTop = player.getY();
        int playerBottom = player.getY() + player.getHeight();

        int tireLeft = tire.getX();
        int tireRight = tire.getX() + tire.getWidth();
        int tireTop = tire.getY();
        int tireBottom = tire.getY() + tire.getHeight();

        return playerRight > tireLeft && playerLeft < tireRight && playerBottom > tireTop && playerTop < tireBottom;
    }

    public static boolean lanternaCheckCollision(GameObject player, GameObject tire) {
        int windowWidth = 500;
        int windowHeight = 400;
        int gridX = 30;
        int gridY = 20;

        int playerX = player.getX() * gridX / windowWidth;
        int playerY = (player.getY() - 5) * gridY / windowHeight;

        int tireX = tire.getX() * gridX / windowWidth;
        int tireY = tire.getY() * gridY / windowHeight;

        return (playerX == tireX && playerY == tireY);
    }
}

