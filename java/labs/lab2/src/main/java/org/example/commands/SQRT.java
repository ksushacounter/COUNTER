package org.example.commands;

import org.example.context.Context;

public class SQRT implements Command {
    public void operation(Context context){
        if (context.getStack().isEmpty()) {
            throw new IllegalStateException("Not enough operands for SQRT");
        }
        Double a = context.getStack().pop();
        context.getStack().push(Math.sqrt(a));
    }
}
