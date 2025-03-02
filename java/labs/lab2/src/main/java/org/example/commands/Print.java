package org.example.commands;


import org.example.context.Context;

public class Print implements Command {
    public void operation(Context context){
         Double num = context.getStack().pop();
         System.out.println(num);
         context.getStack().push(num);
    }
}
