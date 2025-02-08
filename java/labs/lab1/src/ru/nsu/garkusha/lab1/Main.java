package ru.nsu.garkusha.lab1;

import java.util.Scanner;
import java.util.Arrays;

class Main {
    public static void main(String[] args) {
        NumberGenerator generator = new NumberGenerator();
        int[] numbers = generator.numberGeneration();
        int[] guess = new int[4];

        int bulls = 0;
        Scanner scanner = new Scanner(System.in);

        while(bulls != 4) {

            for(int i = 0; i < 4; i++){
                guess[i] = scanner.nextInt();
            }
            GuessChecker Checker = new GuessChecker();
            Checker.checker(guess, numbers);
            System.out.println("вы не угадали!:(");
            System.out.println("коров: " + Checker.cows + " быков: " + Checker.bulls);

            System.out.println("загаданное число: ");
            String numbersPrint = Arrays.toString(numbers).replaceAll("[^1-9]", "");
            System.out.println(numbersPrint);


            System.out.println("ваша догадка: ");
            String guessPrint = Arrays.toString(guess).replaceAll("[^1-9]", "");
            System.out.println(guessPrint);
            bulls = Checker.bulls;

        }
        System.out.println("вы угадали!:)");

    }
}