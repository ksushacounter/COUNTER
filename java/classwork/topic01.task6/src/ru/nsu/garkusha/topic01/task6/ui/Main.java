package ru.nsu.garkusha.topic01.task6.ui;
import ru.nsu.garkusha.topic01.task6.model.*;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        long maxN = scanner.nextLong();
        int k = scanner.nextInt();

        NumberGenerator generator = Factory.createNumberGenerator(maxN);
        PrimeChecker checker = Factory.createPrimeChecker();

        for(int i = 0 ; i < k; i++){
            long number = generator.GetNumber();
            if(checker.isPrime(number)){
                System.out.println(number + " " + "простое");
            }
            else{
                System.out.println(number + " " + "НЕ простое");
            }
        }
    }
}