package ru.nsu.garkusha.topic01.task3.model;

public class RandomGenerator {
    long maxN;

    public RandomGenerator(long maxN){
        this.maxN = maxN;
    };
    public long getNumber() {
        return (long) ((Math.random() * maxN) + 1);
    }
}
