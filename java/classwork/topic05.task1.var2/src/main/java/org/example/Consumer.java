package org.example;

import static java.lang.Thread.sleep;

public class Consumer implements Runnable {
    private int id;
    private Storage<String> storage;
    private int countPutProducts;

    Consumer(int index, Storage<String> storage) {
        this.id = index;
        this.storage = storage;
    }

    public int getCount(){
        return countPutProducts;
    }

    public void run() {
        while (!Thread.interrupted()) {
            try {
                String product = storage.getProduct();
                System.out.println("c" + id + " get object - " + product);
                countPutProducts++;
                sleep(700);
//                if(interrupted()){
//                    System.out.println("Producer " + id + " finished" + " products " + countPutProducts);
//                }
            } catch (InterruptedException e) {
                throw new RuntimeException("Producer " + id + " finished" + " products " + countPutProducts);
            }
        }
        System.out.println("Producer " + id + " finished" + " products " + countPutProducts);

    }
}
