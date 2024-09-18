#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    int len_array = 1700;

    int array[len_array];

    srand(time(NULL));

    for (int i = 0; i < len_array; i++) {
        array[i] = rand() % 100; 
    }

    clock_t start_time = clock();

    for (int i = 0; i < len_array - 1; i++) {
        int counter = 0;
        for (int j = 0; j < len_array - i - 1; j++) {
            if (array[j] > array[j + 1]) {
                int temp = array[j + 1];
                array[j + 1] = array[j];
                array[j] = temp;
                counter += 1;
            }
        }
        if (counter == 0) {
            break;
        }

    }
    clock_t end_time = clock(); 
    double time_spent = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    printf("%f", time_spent);

    for (int i = 0; i < len_array; i++) {
        printf("%d ", array[i]);
    }
return 0;
}
