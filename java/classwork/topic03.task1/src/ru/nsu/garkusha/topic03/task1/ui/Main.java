package ru.nsu.garkusha.topic03.task1.ui;

import ru.nsu.garkusha.topic03.task1.model.CsvReader;

public class Main {
    public static void main(String[] args) {
        String fileName = "C:\\Users\\garku\\IdeaProjects\\k.garkusha\\java\\classwork\\topic03.task1\\src\\example.csv";
        CsvReader Reader = new CsvReader();
        System.out.println(Reader.read(fileName));

    }
}