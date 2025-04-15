package org.example;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;


public class Main {
    public static void main(String[] args) throws IOException {
        Simple simple = new Simple(10, "hi");
        ObjectMapper object = new ObjectMapper();
        File file = new File("simpleJson.json");
        object.writeValue(file, object);
        System.out.println("json создан");
        Simple simple2 = object.readValue(file, Simple.class);
        System.out.println(simple2.getA() + simple2.getB());
    }
}