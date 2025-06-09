package ru.nsu.garkusha;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

public class Processor {
    private static final int saveInterval = 10;
    private static final int queueCapacity = 100;
    private static final int batchSize = 1000;
    private static final Map<String, TickerStats> statsMap = new ConcurrentHashMap<>();
    private static final AtomicBoolean running = new AtomicBoolean(true);
    private static final List<String> OFF = Collections.singletonList("__EOF__");
    private static String input;
    private static String output;
    private static int numThreads;

    public static void main(String[] args) throws Exception {
//        if (args.length != 1) {
//            System.out.println("укажите количество потоков");
//            return;
//        }

        numThreads = Integer.parseInt(args[0]);
        if (numThreads < 1) {
            System.out.println("потоков должно быть >=1");
            return;
        }

        input = args[1];
        output = args[2];

        File inputFile = new File(input);
        if (!inputFile.exists()) {
            System.out.println("Входной файл не найден.");
            return;
        }

        long fileSizeBytes = inputFile.length();
        double fileSizeMB = fileSizeBytes / (1024.0 * 1024.0);
        System.out.printf(Locale.US, "Размер входного файла: %.2f МБ%n", fileSizeMB);

        long startTime = System.currentTimeMillis();

        BlockingQueue<List<String>> queue = new ArrayBlockingQueue<>(queueCapacity);
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);

        ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();
        scheduler.scheduleAtFixedRate(Processor::saveStats, saveInterval, saveInterval, TimeUnit.SECONDS);

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            running.set(false);
            saveStats();
            System.out.println("Обработчик завершает работу...");
        }));

        for (int i = 0; i < numThreads; i++) {
            executor.submit(() -> {
                try {
                    while (true) {
                        List<String> batch = queue.take();
                        if (batch == OFF){
                            break;
                        }

                        for (String line : batch) {
                            processLine(line);
                        }
                    }
                } catch (InterruptedException ignored) {
                }
            });
        }

        try (BufferedReader reader = new BufferedReader(new FileReader(input))) {
            List<String> batch = new ArrayList<>(batchSize);
            String line;
            while ((line = reader.readLine()) != null) {
                batch.add(line);
                if (batch.size() >= batchSize) {
                    queue.put(new ArrayList<>(batch));
                    batch.clear();
                }
            }
            if (!batch.isEmpty()) {
                queue.put(batch);
            }
        }

        for (int i = 0; i < numThreads; i++) {
            queue.put(OFF);
        }

        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.MINUTES);
        scheduler.shutdown();

        long endTime = System.currentTimeMillis();
        saveStats();
        System.out.println("Время обработки: " + (endTime - startTime) + " мс");
    }

    private static void processLine(String line) {
        try {
            String[] parts = line.split(",");
            if (parts.length != 3) return;

            String ticker = parts[1];
            double price = Double.parseDouble(parts[2]);
            long time = Long.parseLong(parts[0]);
            statsMap.computeIfAbsent(ticker, k -> new TickerStats()).update(price, time);
        } catch (Exception ignored) {
        }
    }

    private static synchronized void saveStats() {
        try (BufferedWriter writer = Files.newBufferedWriter(Paths.get(output))) {
            List<String> sortedKeys = statsMap.keySet().stream().sorted().toList();
            for (String ticker : sortedKeys) {
                writer.write("TICKER: " + ticker + " | " + statsMap.get(ticker).getSummary());
                writer.newLine();
            }
        } catch (IOException e) {
            System.err.println("Ошибка при записи статистики: " + e.getMessage());
        }
    }
}
