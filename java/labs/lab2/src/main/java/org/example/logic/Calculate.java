package org.example.logic;

import org.example.commands.Command;
import org.example.context.Contexts;

public class Calculate {

    public static void pushNumber(double num, Contexts context) {
        context.getStack().push(num);
    }

    public static Command makeComand(Contexts context){
        String commandName = context.getLine().get(0);
        return CommandFactory.makeCommand(commandName);
    }

    public static void executeComand(Command command, Contexts context){
        if (command == null) {
            throw new AssertionError("Ошибка: command == null!");
        }
        command.operation(context);
        System.out.println(context.getStack());
    }
}
