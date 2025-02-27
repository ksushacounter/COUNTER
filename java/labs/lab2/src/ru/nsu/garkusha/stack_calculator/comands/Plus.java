package ru.nsu.garkusha.stack_calculator.comands;

import ru.nsu.garkusha.stack_calculator.logic.Command;
import ru.nsu.garkusha.stack_calculator.logic.Context;

public class Plus implements Command {
    @Override
    public void operation(Context context){
        Double a = context.getStack().pop();
        Double b = context.getStack().pop();
        context.getStack().push(a + b);
    }
}
