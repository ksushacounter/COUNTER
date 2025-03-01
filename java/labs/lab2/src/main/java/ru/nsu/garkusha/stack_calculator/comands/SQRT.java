package ru.nsu.garkusha.stack_calculator.comands;

import ru.nsu.garkusha.stack_calculator.logic.Command;
import ru.nsu.garkusha.stack_calculator.logic.Context;

public class SQRT implements Command {
    public void operation(Context context){
        if (context.getStack().isEmpty()) {
            throw new IllegalStateException("Not enough operands for SQRT");
        }
        Double a = context.getStack().pop();
        context.getStack().push(Math.sqrt(a));
    }
}
