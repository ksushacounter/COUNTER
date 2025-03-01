package ru.nsu.garkusha.stack_calculator.logic;
import java.io.FileReader;


import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class MyReader {
    public static String reader(String fileName, Context context){
        try(BufferedReader reader = new BufferedReader(new FileReader(fileName))){
            String line;
            List<String[]> values = new ArrayList<String[]>();
            String currentComand;

            while((line = reader.readLine()) != null){
                if (line.startsWith("#")) {
                    continue;
                }
                values.add(line.split(" "));
            }

            for (String[] value : values) {
                Command comand = Calculate.makeComand(value[0]);
                currentComand = value[0];

                for (String val : value) {
                    if(Types.isDouble(val)) {
                        context.getStack().push(Double.parseDouble(val));
                    }
                    else if(Types.isChar(val) && !Objects.equals(currentComand, val)) {
                        if(context.getDefines().containsKey(val.charAt(0))){
                            context.getStack().push(context.getVal(val.charAt(0)));
                        }
                        else {
                            context.addDefineName(val.charAt(0));
                        }
                    }
                    else if(!Types.isDouble(val) && !Types.isChar(val) && !Objects.equals(currentComand, val)){
                        return "Value " + val + " not identified";
                    }
                }
                Calculate.executeComand(comand, context);
                if (context.takeDefineName() != '0'){
                    throw new IllegalArgumentException("Define " + context.takeDefineName() + " not identified");
                }
            }
        }
        catch (IOException e) {
            throw new RuntimeException(e);
        }
        
        return "Everything is ready";
    }
}
