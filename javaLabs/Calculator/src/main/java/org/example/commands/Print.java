package org.example.commands;


import org.example.context.Contexts;

public class Print implements Command {
    public void operation(Contexts context){
         Double num = context.getStack().pop();
         System.out.println(num);
         context.getStack().push(num);
    }
}
