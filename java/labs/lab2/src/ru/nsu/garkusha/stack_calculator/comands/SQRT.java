package ru.nsu.garkusha.stack_calculator.comands;

import ru.nsu.garkusha.stack_calculator.logic.Comand;
import ru.nsu.garkusha.stack_calculator.logic.Context;

public class SQRT implements Comand {
    public void operation(Context context){
        Double a = context.getStack().pop();
        context.getStack().push(a * a);
    }
}
