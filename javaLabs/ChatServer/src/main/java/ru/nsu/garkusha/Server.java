package ru.nsu.garkusha;

import java.net.*;
import java.util.*;
import java.io.*;
import java.util.concurrent.*;
import java.util.logging.*;

public class Server {
    private static final Logger logger = Logger.getLogger(Server.class.getName());
    private static final Map<String, String> users = new ConcurrentHashMap<>();
    private static final List<ClientHandler> clients = Collections.synchronizedList(new ArrayList<>());
    private static int port;

    public static void main(String[] args) throws IOException {
        if(args.length != 1) {
        port = Config.PORT;
        }
        port = Integer.parseInt(args[0]);
        ServerSocket serverSocket = new ServerSocket(port);
        logger.info("Сервер запущен на порту " + Config.PORT);

        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
        scheduler.scheduleAtFixedRate(() -> {
            synchronized (clients) {
                int before = clients.size();
                clients.removeIf(ch -> ch.socket.isClosed());
                int after = clients.size();
                if (before != after) {
                    logger.info("Очистка неактивных клиентов: удалено " + (before - after));
                }

            }
        }, 10, 10, TimeUnit.SECONDS);

        while (true) {
            Socket clientSocket = serverSocket.accept();
            logger.info("Новое подключение: " + clientSocket.getInetAddress());
            ClientHandler handler = new ClientHandler(clientSocket, users, clients);
            new Thread(handler).start();
        }
    }
}