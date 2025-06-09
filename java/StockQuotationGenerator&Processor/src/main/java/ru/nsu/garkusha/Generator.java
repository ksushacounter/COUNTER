package ru.nsu.garkusha;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

public class Generator {
    private static final String tickersFile = "all_tickers.txt";
    private static final String outputFile = "quotes.csv";
    private static final Random random = new Random();
    private static volatile boolean running = true;

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Укажите количество тикеров для использования");
            return;
        }

        int tickersCount;
        try {
            tickersCount = Integer.parseInt(args[0]);
            if (tickersCount < 1) {
                System.out.println("Количество тикеров должно быть >= 1");
                return;
            }
        } catch (NumberFormatException e) {
            System.out.println("Ошибка: аргумент должен быть целым числом");
            return;
        }

        List<String> tickers;
        try {
            tickers = Files.lines(Paths.get(tickersFile))
                    .filter(line -> !line.isBlank())
                    .map(String::trim)
                    .distinct()
                    .limit(tickersCount)
                    .toList();
        } catch (IOException e) {
            System.err.println("Ошибка при чтении файла с тикерами: " + e.getMessage());
            return;
        }
        System.out.printf("Используются первые %d тикеров из файла.%n", tickersCount);

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            running = false;
            System.out.println("Генератор завершает работу...");
        }));

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile))) {
            long timestamp = System.currentTimeMillis();
            while (running) {
                String ticker = tickers.get(random.nextInt(tickers.size()));
                double price = 10.0 + random.nextDouble() * 1990.0;
                String quote = String.format(Locale.US, "%d,%s,%.2f", timestamp, ticker, price);

                writer.write(quote);
                writer.newLine();

                timestamp += 1 + random.nextInt(100);
            }
            writer.flush();
        } catch (IOException e) {
            System.err.println("Ошибка при записи в файл: " + e.getMessage());
        }
    }
}
