package org.example;

import java.util.ArrayDeque;
import java.util.Queue;
import java.util.concurrent.Semaphore;

import static java.lang.Thread.sleep;

public class Storage<T> {
    private int capacity;
    private Queue<T> products = new ArrayDeque<>();
    private Semaphore forPut;
    private Semaphore forGet;
    private Semaphore access;

    public Storage(int capacity) {
        this.capacity = capacity;
        this.forPut = new Semaphore(capacity);
        this.forGet = new Semaphore(0);
        this.access = new Semaphore(1);
    }

    public Queue<T> getProducts(){
        return products;
    }

    public T getProduct() throws InterruptedException {
        forGet.acquire();
        access.acquire();
        T product = products.poll();
        access.release();
        forPut.release();
        return product;
    }

    public void putProduct(T name) throws InterruptedException {
        forPut.acquire();
        access.acquire();
        products.add(name);
        access.release();
        forGet.release();
    }
}
