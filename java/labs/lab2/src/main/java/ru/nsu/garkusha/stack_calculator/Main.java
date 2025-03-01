package ru.nsu.garkusha.stack_calculator;

import ru.nsu.garkusha.stack_calculator.logic.*;

import java.util.Objects;
import java.util.Scanner;
//😎🤠🐗🐸🐧🐧🐧🐌🐛🐛🦇🪰🦾👩🏽🎀🎀
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Context context = new Context();

        String firstLine = scanner.nextLine();

        if (firstLine.endsWith(".txt")) {
            System.out.println("read from file");
            System.out.println(MyReader.reader(firstLine, context));
        } else {
            String line = "";
            String[] parsedLine;
            String currentComand;

            while (!(Objects.equals((line = scanner.nextLine()), "stop"))) {
                if (line.startsWith("#")) {
                    continue;
                }
                parsedLine = line.split(" ");
                Command command = Calculate.makeComand(parsedLine[0]);
                currentComand = parsedLine[0];

                for (String val : parsedLine) {
                    if (Types.isDouble(val)) {
                        context.getStack().push(Double.parseDouble(val));
                    } else if (Types.isChar(val) && !Objects.equals(currentComand, val)) {
                        if (context.getDefines().containsKey(val.charAt(0))) {
                            context.getStack().push(context.getVal(val.charAt(0)));
                        } else {
                            context.addDefineName(val.charAt(0));
//                            return ("Define " + val + " not specified");
                        }
                    } else if (!Types.isDouble(val) && !Types.isChar(val) && !Objects.equals(currentComand, val)) {
                        System.out.println("Value " + val + " not identified");
                    }
                }
                Calculate.executeComand(command, context);
            }


        }
        System.out.println("Everything is ready");
    }
}


