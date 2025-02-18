package ru.nsu.garkusha.lab1;


import java.util.Arrays;

public class NumberGenerator {
    int[] numbers;
    int count = 0;

    public NumberGenerator() {
        numbers = new int[4];
    }

    public String numberGeneration() {
        while (count != 4) {
            int current_number = (int) (Math.random() * 10) + 1;
            int flag = 0;
            for (int i : numbers) {
                if(current_number == i){
                    flag = 1;
                }
            }
            if (flag == 0) {
                numbers[count] = current_number;
                count++;
            }
        }
        return Arrays.toString(numbers).replaceAll("[^1-9]","");
    }
}
