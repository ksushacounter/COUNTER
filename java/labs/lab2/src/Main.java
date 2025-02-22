import ru.nsu.garkusha.stack_calculator.logic.Calculate;
import ru.nsu.garkusha.stack_calculator.logic.Context;
import ru.nsu.garkusha.stack_calculator.logic.MyReader;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Context context = new Context();

        String firstLine = scanner.next();

        if (firstLine.endsWith(".txt")) {
            System.out.println("read from file");
            MyReader.reader(firstLine, context);
        }

        else{
            while (scanner.hasNext()) {
                if (scanner.hasNextDouble()) {
                    Calculate.pushNumber(scanner.nextDouble(), context);
                    System.out.println("число");
                }
                else {
                    String command = scanner.next();
                    System.out.println(command);
                    Calculate.executeComand(command, context);
                }
            }
        }
    }
}