package ru.nsu.garkusha.stack_calculator.logic;

import ru.nsu.garkusha.stack_calculator.comands.*;

public class ComandFactory {
    public static Comand makeComand(String comandName){
        return switch (comandName) {
            case "+" -> new Plus();
            case "-" -> new Minus();
            case "*" -> new Multiplication();
            case "/" -> new Division();
            case "SQRT" -> new SQRT();
            default -> null; //exeption
        };
    }
}
