package org.example;

import static java.lang.Thread.sleep;

public class Producer implements Runnable{
    private int id;
    private Storage<String> storage;
    private int countProducts = 0;

    public Producer(int id, Storage<String> storage){
        this.id = id;
        this.storage = storage;
    }

    public void run(){
        while(!Thread.interrupted()){
            String product = "p " + id + ": " + countProducts++;
            try {
                storage.putProduct(product);
                System.out.println("p " + id + " put object - " + product);
                sleep(500);
            } catch (InterruptedException e) {
                throw new RuntimeException("Producer " + id + " finished");
            }

        }
    }
}
