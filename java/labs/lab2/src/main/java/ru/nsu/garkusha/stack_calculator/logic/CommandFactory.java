package ru.nsu.garkusha.stack_calculator.logic;

import ru.nsu.garkusha.stack_calculator.comands.*;

public class CommandFactory {
    public static Command makeCommand(String commandName){
        return switch (commandName) {
            case "+" -> new Plus();
            case "-" -> new Minus();
            case "*" -> new Multiplication();
            case "/" -> new Division();
            case "SQRT" -> new SQRT();
            case "DEFINE" -> new Define();
            case "PRINT" -> new Print();
            case "PUSH" -> new Push();
            case "POP" -> new Pop();
            default -> null; //exception
        };
    }
}
