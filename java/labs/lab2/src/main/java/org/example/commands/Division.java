package org.example.commands;


import org.example.context.Context;

public class Division implements Command {
    public void operation(Context context){
        if (context.getStack().size() < 2) {
            throw new IllegalStateException("Not enough operands for division");
        }
        Double divisor = context.getStack().pop();
        Double divident = context.getStack().pop();
        if (divisor == 0.0) {
            throw new ArithmeticException("Division by zero");
        }
        context.getStack().push(divident / divisor);
    }
}
