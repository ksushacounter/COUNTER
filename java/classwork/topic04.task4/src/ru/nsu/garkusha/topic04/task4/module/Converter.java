package ru.nsu.garkusha.topic04.task4.module;

public interface Converter <T extends Number>{
    String convert(T x);
}
