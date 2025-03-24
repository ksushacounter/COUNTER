package org.example;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Scanner scanner = new Scanner(System.in);
        System.out.println("N:");
        int capacity = scanner.nextInt();
        System.out.print("P:");
        
        int P = scanner.nextInt();
        System.out.print("C:");
        int C = scanner.nextInt();
        System.out.print("T:");
        int T = scanner.nextInt();

        Storage<String> storage = new Storage<>(capacity);

        Thread[] producers = new Thread[P];
        for (int i = 0; i < P; i++) {
            producers[i] = new Thread(new Producer(i, storage));
            producers[i].start();
        }

        Thread[] consumers = new Thread[C];
        for (int i = 0; i < C; i++) {
            consumers[i] = new Thread(new Consumer(i, storage));
            consumers[i].start();
        }

        Thread.sleep(T * 1000L);

        for (int i = 0; i < P; i++) {
//            System.out.println(producers[i].getCount());
            producers[i].interrupt();
            producers[i].join();
        }
        System.out.println("P died");

        for (int i = 0; i < C; i++) {
//            System.out.println(consumers[i].getCount());
            consumers[i].interrupt();
            consumers[i].join();
        }
        System.out.println("C died");

        storage.deleteProducts();
        System.out.println("Storage free");

        System.exit(0);
    }
}