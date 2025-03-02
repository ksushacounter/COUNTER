package org.example;

import org.example.commands.*;
import org.example.context.Context;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class OperationTest {
    private Context context;

    @BeforeEach
    public void setUp() {
        context = new Context();
    }

    /*** 🎀 Арифметические операции ***/

    @Test
    public void testPlus() {
        context.getStack().push(3.0);
        context.getStack().push(2.0);
        new Plus().operation(context);
        Assertions.assertEquals(5.0, context.getStack().pop());
    }

    @Test
    public void testMinus() {
        context.getStack().push(10.0);
        context.getStack().push(4.0);
        new Minus().operation(context);
        Assertions.assertEquals(6.0, context.getStack().pop());
    }

    @Test
    public void testMultiplication() {
        context.getStack().push(3.0);
        context.getStack().push(5.0);
        new Multiplication().operation(context);
        Assertions.assertEquals(15.0, context.getStack().pop());
    }

    @Test
    public void testDivision() {
        context.getStack().push(10.0);
        context.getStack().push(2.0);
        new Division().operation(context);
        Assertions.assertEquals(5.0, context.getStack().pop());
    }

    @Test
    public void testDivisionByZero() {
        context.getStack().push(10.0);
        context.getStack().push(0.0);
        Assertions.assertThrows(ArithmeticException.class, () -> new Division().operation(context));
    }

    /*** 🤙🏽🤙🏽🤙🏽 Операции со стеком ***/

    @Test
    public void testPush() {
        context.getStack().push(555.5);
        new Push().operation(context);
        Assertions.assertEquals(555.5, context.getStack().pop());
    }

    @Test
    public void testPop() {
        context.getStack().push(777.7);
        new Pop().operation(context);
        Assertions.assertTrue(context.getStack().isEmpty());
    }

    @Test
    public void testPopFromEmptyStack() {
        Assertions.assertThrows(IllegalStateException.class, () -> new Pop().operation(context));
    }

    /*** 🖨️ Вывод ***/

    @Test
    public void testPrint() {
        context.getStack().push(777.7);
        Print print = new Print();
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        PrintStream realOutput = System.out;
        System.setOut(new PrintStream(outputStream));
        print.operation(context);
        Assertions.assertEquals("777.7", outputStream.toString().trim());
        Assertions.assertEquals(1, context.getStack().size());
        Assertions.assertEquals(777.7, context.getStack().peek());
        System.setOut(realOutput);
    }

    @Test
    public void testDefine() {
        context.addDefineName('a');
        context.getStack().push(555.5);
        new Define().operation(context);
        Assertions.assertEquals(555.5, context.getDefines().get('a'));
    }
}
