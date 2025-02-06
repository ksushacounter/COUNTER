package ru.nsu.garkusha.topic01.task6.model;

public class PrimeCheckerReal {
    public boolean isPrime(long n){
        if(n == 2){
            return false;
        }
        for(int i = 2; i < n-1; i++){
            if(n%i == 0){
                return false;
            }
        }
    return true;
    }
}
