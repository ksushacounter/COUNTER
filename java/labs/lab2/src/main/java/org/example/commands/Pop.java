package org.example.commands;


import org.example.context.Context;

public class Pop implements Command {

    @Override
    public void operation(Context context) {
        if (context.getStack().isEmpty()) {
            throw new IllegalStateException("Not enough operands for addition");
        }
        context.getStack().pop();
    }
}
