package ru.nsu.garkusha.stack_calculator.comands;

import ru.nsu.garkusha.stack_calculator.logic.Comand;

import java.util.Stack;

public class Minus implements Comand {
    @Override
    public void operation(Stack<Double> stack){
        Double a = stack.pop();
        Double b = stack.pop();
        stack.push(a - b);
    }
}
