package ru.nsu.garkusha.topic01.task6.model;

public class Factory {
    public static NumberGeneratorReal createNumberGenerator(long maxN) {
        return new NumberGeneratorReal(maxN);
    }

    public static PrimeChecker createPrimeChecker() {
        return new PrimeCheckerReal();
    }
}

