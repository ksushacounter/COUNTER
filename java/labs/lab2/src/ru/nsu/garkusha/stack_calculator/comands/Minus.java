package ru.nsu.garkusha.stack_calculator.comands;

import ru.nsu.garkusha.stack_calculator.logic.Comand;
import ru.nsu.garkusha.stack_calculator.logic.Context;

import java.util.Stack;

public class Minus implements Comand {
    @Override
    public void operation(Context context){
        Double a = context.getStack().pop();
        Double b = context.getStack().pop();
        context.getStack().push(a - b);
    }
}
