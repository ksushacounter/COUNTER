package org.example;

import static java.lang.Thread.sleep;

public class Consumer implements Runnable{
    private int id;
    private Storage<String> storage;

    Consumer(int index, Storage<String> storage){
        this.id = index;
        this.storage = storage;
    }

    public void run(){
        while (!Thread.interrupted()){
            try {
                String product = storage.getProduct();
                System.out.println("c " + id + " get object - " + product);
                sleep(700);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }

        }
    }
}
