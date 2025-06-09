package ru.nsu.garkusha;

import java.io.*;
import java.util.*;

public class MessageParser {
    public static Map<String, String> readMessage(BufferedReader in) throws IOException {
        Map<String, String> map = new HashMap<>();
        StringBuilder value = new StringBuilder();
        String currentKey = null;
        String line;
        while ((line = in.readLine()) != null) {
            if (line.isEmpty()) break;
            if (line.startsWith("  ")) {
                value.append("\n").append(line.substring(2));
            } else {
                if (currentKey != null) {
                    map.put(currentKey.toLowerCase(), value.toString());
                }
                int colonIndex = line.indexOf(": ");
                if (colonIndex == -1) continue;
                currentKey = line.substring(0, colonIndex).toLowerCase();
                value = new StringBuilder(line.substring(colonIndex + 2));
            }
        }
        if (currentKey != null) {
            map.put(currentKey.toLowerCase(), value.toString());
        }
        return map;
    }

    public static void sendMessage(PrintWriter out, Map<String, String> fields) {
        for (Map.Entry<String, String> entry : fields.entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();
            if (value.contains("\n")) {
                String[] lines = value.split("\n");
                out.println(key + ": " + lines[0]);
                for (int i = 1; i < lines.length; i++) {
                    out.println("  " + lines[i]);
                }
            } else {
                out.println(key + ": " + value);
            }
        }
        out.println();
        out.flush();
    }
}