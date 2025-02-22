package ru.nsu.garkusha.stack_calculator.logic;

import java.util.Stack;

public class Context {
    private Stack<Double> stack;

    public Context(){
        this.stack = new Stack<Double>();
    }

    public Stack<Double> getStack(){
        return stack;
    }
}
