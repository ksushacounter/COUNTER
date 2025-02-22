package ru.nsu.garkusha.stack_calculator.logic;
import java.io.FileNotFoundException;
import java.io.FileReader;


import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class MyReader {
    public static boolean isDouble(String value){
        try{
            Double a = Double.parseDouble(value);
            return true;
        }
        catch (NumberFormatException e){
            return false;
        }


    }
    public static void reader(String fileName, Context context){
        try(BufferedReader reader = new BufferedReader(new FileReader(fileName))){
            String line;
            List<String[]> values = new ArrayList<String[]>();

            while((line = reader.readLine()) != null){
                if (line.startsWith("#") || line.isEmpty()) {
                    continue;
                }
                values.add(line.split(" "));
            }

            for (String[] value : values) {
                for (String val : value) {
                    if(isDouble(val)){
                        context.getStack().push(Double.parseDouble(val));
                    }
                    else{
                        Calculate.executeComand(val, context);
                    }
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }
}
