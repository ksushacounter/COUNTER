package ru.nsu.garkusha;

import java.net.*;
import java.io.*;
import java.security.*;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.logging.*;

public class ClientHandler implements Runnable {
    final Socket socket;
    private final Map<String, String> users;
    private final List<ClientHandler> clients;
    private PrintWriter out;
    private String name;
    private static final Logger logger = Logger.getLogger(ClientHandler.class.getName());
    private static final Map<String, FileInfo> files = new ConcurrentHashMap<>();

    private static class FileInfo {
        String name;
        String mimeType;
        byte[] content;

        FileInfo(String name, String mimeType, byte[] content) {
            this.name = name;
            this.mimeType = mimeType;
            this.content = content;
        }
    }

    public ClientHandler(Socket socket, Map<String, String> users, List<ClientHandler> clients) {
        this.socket = socket;
        this.users = users;
        this.clients = clients;
    }

    @Override
    public void run() {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream(), "UTF-8"));
            out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream(), "UTF-8"));

            while (true) {
                Map<String, String> msg = MessageParser.readMessage(in);
                if (!"login".equalsIgnoreCase(msg.get("command"))) {
                    sendError("Login required");
                    logger.warning("Клиент не авторизовался перед отправкой команды");
                    continue;
                }
                String username = msg.get("name");
                String password = msg.get("password");
                if (username == null || password == null) {
                    sendError("Missing credentials");
                    logger.warning("Не указаны имя пользователя или пароль");
                    continue;
                }
                String hash = hash(password);
                String saved = users.get(username);
                if (saved == null) {
                    users.put(username, hash);
                    logger.info("Новый пользователь зарегистрирован: " + username);
                } else if (!saved.equals(hash)) {
                    sendError("Wrong password");
                    logger.warning("Неверный пароль для пользователя: " + username);
                    socket.close();
                    return;
                }
                name = username;
                sendSuccess();
                logger.info("Пользователь " + name + " успешно авторизовался");
                break;
            }

            synchronized (clients) {
                clients.add(this);
                broadcast(event("userlogin", name));
                logger.info("Пользователь " + name + " добавлен в чат. Всего пользователей: " + clients.size());
            }

            while (true) {
                Map<String, String> msg = MessageParser.readMessage(in);
                String command = msg.get("command");
                if (command == null) continue;
                switch (command.toLowerCase()) {
                    case "message":
                        String text = msg.get("message");
                        if (text == null) {
                            sendError("No message");
                            logger.warning("Пустое сообщение от " + name);
                            break;
                        }
                        Map<String, String> message = new HashMap<>();
                        message.put("Event", "message");
                        message.put("From", name);
                        message.put("Message", text);
                        broadcast(message);
                        sendSuccess();
                        logger.info("Сообщение от " + name + ": " + text);
                        break;

                    case "upload":
                        String fileName = msg.get("name");
                        String mimeType = msg.get("mimetype");
                        String encoding = msg.get("encoding");
                        String content = msg.get("content");
                        if (fileName == null || mimeType == null || encoding == null || content == null) {
                            sendError("Missing file data");
                            logger.warning("Недостаточно данных для загрузки файла от " + name);
                            break;
                        }
                        if (!"base64".equalsIgnoreCase(encoding)) {
                            sendError("Unsupported encoding");
                            logger.warning("Неподдерживаемый формат кодирования от " + name);
                            break;
                        }
                        try {
                            byte[] fileContent = Base64.getDecoder().decode(content);
                            String fileId = UUID.randomUUID().toString();
                            files.put(fileId, new FileInfo(fileName, mimeType, fileContent));
                            Map<String, String> response = new HashMap<>();
                            response.put("Status", "Success");
                            response.put("FileId", fileId);
                            MessageParser.sendMessage(out, response);
                            Map<String, String> fileEvent = new HashMap<>();
                            fileEvent.put("Event", "file");
                            fileEvent.put("FileId", fileId);
                            fileEvent.put("From", name);
                            fileEvent.put("Name", fileName);
                            fileEvent.put("Size", String.valueOf(fileContent.length));
                            fileEvent.put("MimeType", mimeType);
                            broadcast(fileEvent);
                            logger.info("Файл загружен: " + fileName + " (ID: " + fileId + ")");
                        } catch (IllegalArgumentException e) {
                            sendError("Invalid Base64 content");
                            logger.warning("Неверный Base64-контент от " + name);
                        }
                        break;

                    case "download":
                        String fileId = msg.get("fileid");
                        if (fileId == null) {
                            sendError("Missing FileId");
                            logger.warning("Отсутствует FileId в запросе от " + name);
                            break;
                        }
                        FileInfo fileInfo = files.get(fileId);
                        if (fileInfo == null) {
                            sendError("File not found");
                            logger.warning("Файл не найден: " + fileId);
                            break;
                        }
                        Map<String, String> fileResponse = new HashMap<>();
                        fileResponse.put("Status", "Success");
                        fileResponse.put("FileId", fileId);
                        fileResponse.put("Name", fileInfo.name);
                        fileResponse.put("MimeType", fileInfo.mimeType);
                        fileResponse.put("Encoding", "base64");
                        fileResponse.put("Content", Base64.getEncoder().encodeToString(fileInfo.content));
                        MessageParser.sendMessage(out, fileResponse);
                        logger.info("Файл отправлен пользователем " + name + ": " + fileInfo.name);
                        break;

                    case "logout":
                        sendSuccess();
                        socket.close();
                        logger.info("Пользователь " + name + " вышел из чата");
                        return;

                    case "list":
                        Map<String, String> list = new HashMap<>();
                        list.put("Status", "Success");
                        list.put("Usercount", String.valueOf(clients.size()));
                        int i = 1;
                        for (ClientHandler ch : clients) {
                            list.put("Username" + i, ch.name);
                            i++;
                        }
                        MessageParser.sendMessage(out, list);
                        logger.fine("Запрос списка пользователей от " + name);
                        break;

                    case "plus":
                        String operands = msg.get("plus");

//                        String[] parts = operands.split(" ");
//                        for (int j = 0; j < parts.length - 1; j += 2) {
//                            String key = parts[j].replace(":", "");
//                            int value = Integer.parseInt(parts[j + 1]);
//                            values.put(key, value);
//                        }
                        int x = Integer.parseInt(msg.get("x"));
                        int y = Integer.parseInt(msg.get("y"));
                        int result = x + y;

                        Map<String, String> sum = new HashMap<>();
                        sum.put("Event", "plus");
                        sum.put("Result", String.valueOf(result));
                        sendToUser(name, sum);
                        sendSuccess();
                        logger.fine("Запрос суммы чисел от " + name);
                        break;
                }
            }
        } catch (Exception e) {
            logger.severe("Ошибка в обработчике клиента: " + e.getMessage());
            e.printStackTrace();
        } finally {
            try {
                socket.close();
            } catch (IOException e) {
                logger.warning("Ошибка при закрытии сокета: " + e.getMessage());
            }
            clients.remove(this);
            if (name != null) {
                broadcast(event("userlogout", name));
                logger.info("Пользователь " + name + " отключился");
            }
        }
    }

    private void broadcast(Map<String, String> msg) {
        synchronized (clients) {
            for (ClientHandler ch : clients) {
                MessageParser.sendMessage(ch.out, msg);
            }
        }
    }

    private void sendToUser(String username, Map<String, String> msg) {
        synchronized (clients) {
            for (ClientHandler ch : clients) {
                if (username.equals(ch.name)) {
                    MessageParser.sendMessage(ch.out, msg);
                    break;
                }
            }
        }
    }


    private void sendSuccess() {
        Map<String, String> msg = new HashMap<>();
        msg.put("Status", "Success");
        MessageParser.sendMessage(out, msg);
    }

    private void sendError(String reason) {
        Map<String, String> msg = new HashMap<>();
        msg.put("Status", "Error");
        msg.put("Message", reason);
        MessageParser.sendMessage(out, msg);
    }

    private Map<String, String> event(String type, String user) {
        Map<String, String> msg = new HashMap<>();
        msg.put("Event", type);
        msg.put("Username", user);
        return msg;
    }

    private String hash(String s) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        return Base64.getEncoder().encodeToString(md.digest(s.getBytes("UTF-8")));
    }
}