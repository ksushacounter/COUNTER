package ru.nsu.garkusha.stack_calculator.comands;

import ru.nsu.garkusha.stack_calculator.logic.Command;
import ru.nsu.garkusha.stack_calculator.logic.Context;

public class Define implements Command {
    public void operation(Context context){
        Character name = context.takeDefineName();
        context.addDefineName('0');
        Double val = context.getStack().pop();
        context.newDefine(name, val);
    }
}
