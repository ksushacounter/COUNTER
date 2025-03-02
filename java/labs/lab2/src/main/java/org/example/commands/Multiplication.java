package org.example.commands;


import org.example.context.Context;

public class Multiplication implements Command {
    public void operation(Context context){
        if (context.getStack().size() < 2) {
            throw new IllegalStateException("Not enough operands for multiplication");
        }
        Double a = context.getStack().pop();
        Double b = context.getStack().pop();
        context.getStack().push(a * b);
    }
}
