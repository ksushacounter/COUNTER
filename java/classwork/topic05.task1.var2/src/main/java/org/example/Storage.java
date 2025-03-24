package org.example;

import java.util.ArrayDeque;
import java.util.Queue;

import static java.lang.Thread.sleep;

public class Storage<T> {
    private final int capacity;
    private final Queue<T> products = new ArrayDeque<>();
    private int countProducts;

    Storage(int capacity) {
        this.capacity = capacity;
    }

    public synchronized void deleteProducts(){
        products.clear();
        System.out.println(countProducts + "products was passed through the vault");
        notifyAll();
    }

    public synchronized T getProduct() throws InterruptedException {
        while(products.isEmpty()){
            wait();
        }
        T product = products.poll();
        countProducts++;
        notifyAll();
        return product;
    }

    public synchronized void putProduct(T name) throws InterruptedException {
        while(products.size() == capacity){
            wait();
        }
        products.add(name);
        notifyAll();
    }
}
