package org.example;

import static java.lang.Thread.sleep;

public class Producer implements Runnable {
    private int id;
    private Storage<String> storage;
    private int countGetProducts = 0;

    public Producer(int id, Storage<String> storage) {
        this.id = id;
        this.storage = storage;
    }

    public int getCount(){
        return countGetProducts;
    }

    public void run() {
        while (!Thread.interrupted()) {
            String product = "p " + id + ": ";
            try {
                storage.putProduct(product);
                countGetProducts++;
                System.out.println("p" + id + " put object - " + product);
                sleep(500);
//                if(interrupted()){
//                    System.out.println("Producer " + id + " finished" + " products " + countGetProducts);
//                }
            } catch (InterruptedException e) {
                throw new RuntimeException("Producer " + id + " finished" + " products " + countGetProducts);
            }
        }
//        System.out.println("Producer " + id + " finished" + " products " + countGetProducts);
    }
}
