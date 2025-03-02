package org.example.logic;

import org.example.commands.Command;
import org.example.context.Context;

public class Calculate {

    public static void pushNumber(double num, Context context) {
        context.getStack().push(num);
    }

    public static Command makeComand(String commandName){
        return CommandFactory.makeCommand(commandName);
    }

    public static void executeComand(Command comand, Context context){
        if (comand == null) {
            throw new AssertionError("Ошибка: comand == null!");
        }
        comand.operation(context);
        System.out.println(context.getStack());
    }
}
