package ru.nsu.garkusha.topic04.task4.module;

import java.util.TreeMap;

public class ConvertToRoman implements Converter{
    @Override
    public String convert(Number x) {
        Number l = ToRoman.map.floorKey(x);
        if ( x == l ) {
            return ToRoman.map.get(x);
        }
        Number next = ((int)x) - ((int)l);
        return ToRoman.map.get(l) + convert((Number) next);
    }
}
