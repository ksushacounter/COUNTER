package ru.nsu.garkusha.topic03.task1.model;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class CsvReader {
    private boolean isNumeric(String str) {
        try {
            Integer.parseInt(str);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }
    public int read(String fileName) {
        int countInt = 0;
        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            String line;
            List<String[]> values = new ArrayList<>();

           while ((line = reader.readLine()) != null) {
               values.add(line.split(","));
           }



            for (String[] value : values) {
                for (String val : value) {
                    System.out.println(val);

                    if (isNumeric(val)) {
                        countInt += Integer.parseInt(val);
                    }
                }
            }
        }
        catch (IOException e) {
            e.printStackTrace();
        }
        return countInt;

    }
}
