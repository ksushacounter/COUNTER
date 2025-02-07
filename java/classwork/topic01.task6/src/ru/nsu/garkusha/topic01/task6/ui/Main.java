package ru.nsu.garkusha.topic01.task6.ui;
import ru.nsu.garkusha.topic01.task6.model.Factory;
import ru.nsu.garkusha.topic01.task6.model.NumberGeneratorReal;
import ru.nsu.garkusha.topic01.task6.model.PrimeCheckerReal;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        long maxN = scanner.nextLong();
        int k = scanner.nextInt();

        NumberGeneratorReal generator = Factory.createNumberGenerator(maxN);
        PrimeCheckerReal checker = Factory.createPrimeChecker();

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