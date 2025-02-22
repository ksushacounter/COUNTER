package ru.nsu.garkusha.stack_calculator.logic;

import jdk.dynalink.Operation;

import java.util.Stack;

public class Calculate {

    public static void pushNumber(double num, Context context) {
        context.getStack().push(num);
    }

    public static void executeComand(String comandName, Context context){
        Comand comand = ComandFactory.makeComand(comandName);
        if (comand == null) {
            throw new AssertionError("Ошибка: comand == null!");
        }
        comand.operation(context);
        System.out.println(context.getStack());
    }
}
