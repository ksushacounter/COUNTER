package ru.nsu.garkusha.lab1;


public class NumberGenerator {
    int[] numbers;
    int count = 0;

    NumberGenerator() {
        numbers = new int[4];
    }

    int[] numberGeneration() {
        while (count != 4) {
            int current_number = (int) (Math.random() * 9) + 1;
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
        return numbers;
    }
}
