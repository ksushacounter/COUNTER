package ru.nsu.garkusha.stack_calculator.comands;

import ru.nsu.garkusha.stack_calculator.logic.Command;
import ru.nsu.garkusha.stack_calculator.logic.Context;

public class Print implements Command {
    public void operation(Context context){
         Double num = context.getStack().pop();
         System.out.println(num);
         context.getStack().push(num);
    }
}
