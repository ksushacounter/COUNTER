package org.example.model;

public class GuessChecker {
    private int cows = 0;
    private int bulls = 0;

    public int getCows() {
        return cows;
    }

    public int getBulls() {
        return bulls;
    }

    public void checker(String guess, String numbers) {
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                if(numbers.charAt(i) == guess.charAt(j)){
                    cows++;
                }
                if(numbers.charAt(i) == guess.charAt(j) && i == j){
                    bulls++;
                    cows--;
                }

            }
        }
    }
}

