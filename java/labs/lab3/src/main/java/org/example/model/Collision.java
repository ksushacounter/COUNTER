package org.example.model;

public class Collision {
    public static boolean checkCollision(GameObject player, GameObject tire){
        int playerLeft = player.getX();
        int playerRight = player.getX() + player.getWidth();
        int playerTop = player.getY();
        int playerBottom = player.getY() + player.getHeight();

        int tireLeft = tire.getX();
        int tireRight = tire.getX() + tire.getWidth();
        int tireTop = tire.getY();
        int tireBottom = tire.getY() + tire.getHeight();

        boolean boom = playerRight > tireLeft && playerLeft < tireRight && playerBottom > tireTop && playerTop < tireBottom;
        if(boom){
            System.out.println("boom");
        }
        return boom;
    }
}
