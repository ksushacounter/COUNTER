package org.example.module;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class Storage <T>{
    private int capacity;
    List<String> products = new ArrayList<String>();

    Storage(int capacity){
        this.capacity = capacity;
    }
    public void getProduct(String name){
        for (int i = 0; i < capacity; i++){
            if(Objects.equals(products.get(i), name)){
                products.remove(name);
            }
        }
    }
    public void putProduct(String name){
        products.add(name);
        while(products.size() == capacity){

        }
    }
}
