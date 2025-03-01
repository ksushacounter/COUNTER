package ru.nsu.garkusha.stack_calculator.comands;

import ru.nsu.garkusha.stack_calculator.logic.Command;
import ru.nsu.garkusha.stack_calculator.logic.Context;

public class Minus implements Command {
    @Override
    public void operation(Context context){
        if (context.getStack().size() < 2) {
            throw new IllegalStateException("Not enough operands for subtraction");
        }
        Double difference = context.getStack().pop();
        Double integer = context.getStack().pop();
        context.getStack().push(integer - difference);
    }
}
