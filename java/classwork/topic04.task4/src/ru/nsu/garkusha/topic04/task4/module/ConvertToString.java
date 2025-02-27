package ru.nsu.garkusha.topic04.task4.module;

public class ConvertToString implements Converter{

    @Override
    public String convert(Number x) {
        return x.toString();
    }
}
