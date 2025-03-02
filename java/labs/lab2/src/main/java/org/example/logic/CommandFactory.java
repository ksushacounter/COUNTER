package org.example.logic;


import org.example.commands.*;

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
            case "POP" -> new Pop();
            default -> null; //exception
        };
    }
}
