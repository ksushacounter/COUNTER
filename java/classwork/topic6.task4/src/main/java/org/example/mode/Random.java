package org.example.mode;

public class Random {
    public static String getNumber(){
        Double random = (Math.random() * 6) + 1;
        String romanRandom = Translate.toRoman(Integer.getInteger(String.valueOf(random)));
        return romanRandom;
    }
}
