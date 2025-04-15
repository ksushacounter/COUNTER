package ru.nsu.garkusha.lab1;

import java.util.Scanner;

class Main {
    public static void main(String[] args) {
        NumberGenerator generator = new NumberGenerator();
        String numbers = generator.numberGeneration();

        int bulls = 0;
        Scanner scanner = new Scanner(System.in);

        while(true) {
            String guess = scanner.nextLine();

            GuessChecker Checker = new GuessChecker();
            Checker.checker(guess, numbers);
            bulls = Checker.bulls;

            if(bulls != 4) {
                System.out.println("вы не угадали!:(");
                System.out.println("коров: " + Checker.cows + " быков: " + Checker.bulls);

                System.out.println("догадка: ");
                System.out.println(guess);

                System.out.println("загаданное число: ");
                System.out.println(numbers);
            }
            else{
                break;
            }

        }
        System.out.println("вы угадали!:)");

    }
}