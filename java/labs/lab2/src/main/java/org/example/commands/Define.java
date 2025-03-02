package org.example.commands;

import org.example.context.Context;

public class Define implements Command {
    public void operation(Context context){
        Character name = context.takeDefineName();
        context.addDefineName('0');
        Double val = context.getStack().pop();
        context.newDefine(name, val);
    }
}
