package ru.nsu.garkusha.lab1;

public class GuessChecker {
    int cows = 0;
    int bulls = 0;
    void checker(int[] guess, int[] numbers) {
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                if(numbers[i] == guess[j]){
                    cows++;
                }
                if(numbers[i] == guess[j] && i == j){
                    bulls++;
                    cows--;
                }

            }
        }
    }
}
