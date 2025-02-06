package ru.nsu.garkusha.topic01.task6.model;

public class NumberGeneratorReal implements NumberGenerator{
    long maxN;

    NumberGeneratorReal(long maxN){
        this.maxN = maxN;
    };
    public long GetNumber(){
        return(long) ((Math.random()*maxN) + 1);
    }
}
