package ru.nsu.garkusha;

import java.io.*;
import java.net.*;
import java.nio.file.*;
import java.security.*;
import java.util.*;
import java.util.concurrent.*;

public class Client {
    private volatile Socket socket;
    private PrintWriter out;
    private BufferedReader in;
    private String username;
    private volatile boolean loggedIn = false;
    private final ExecutorService executorService = Executors.newFixedThreadPool(2);
    private final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
    private final ClientGUI gui;

    public Client(ClientGUI gui) {
        this.gui = gui;
    }

    public void login(String ip, int port, String name, String password) {
        if (name.isEmpty() || password.isEmpty() || ip.isEmpty() || port <= 0) {
            gui.showError("Заполните все поля");
            return;
        }

        executorService.execute(() -> {
            try {
                socket = new Socket();
                socket.connect(new InetSocketAddress(ip, port), 3000);
                socket.setSoTimeout(5000);

                out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream(), "UTF-8"), true);
                in = new BufferedReader(new InputStreamReader(socket.getInputStream(), "UTF-8"));

                Map<String, String> loginMsg = new HashMap<>();
                loginMsg.put("Command", "login");
                loginMsg.put("Name", name);
                loginMsg.put("Password", hash(password));
                MessageParser.sendMessage(out, loginMsg);

                Map<String, String> response = MessageParser.readMessage(in);
                if ("Success".equalsIgnoreCase(response.get("status"))) {
                    username = name;
                    loggedIn = true;
                    gui.switchToChatPanel();
                    executorService.execute(this::receiveMessages);
                    updateUserList();
                    scheduler.scheduleAtFixedRate(this::updateUserList, 10, 10, TimeUnit.SECONDS);
                } else {
                    String error = response.get("message");
                    gui.showError(error != null ? error : "Ошибка входа");
                    disconnect();
                }
            } catch (SocketTimeoutException e) {
                gui.showError("Таймаут подключения к серверу");
            } catch (ConnectException e) {
                gui.showError("Не удалось подключиться к серверу");
            } catch (Exception e) {
                gui.showError("Ошибка подключения: " + e.getMessage());
                e.printStackTrace();
            }
        });
    }

    public void updateUserList() {
        executorService.execute(() -> {
            try {
                Map<String, String> msg = new HashMap<>();
                msg.put("Command", "list");
                MessageParser.sendMessage(out, msg);
            } catch (Exception e) {
                gui.showError("Ошибка получения списка пользователей: " + e.getMessage());
                disconnect();
            }
        });
    }

    public void sendMessage(String text) {
        if (!loggedIn || text.trim().isEmpty()) return;

        executorService.execute(() -> {
            try {
                Map<String, String> msg = new HashMap<>();
                msg.put("Command", "message");
                msg.put("Message", text);
                MessageParser.sendMessage(out, msg);
                gui.clearMessageField();
            } catch (Exception e) {
                gui.showError("Ошибка отправки сообщения: " + e.getMessage());
                disconnect();
            }
        });
    }

    public void uploadFile(File file) {
        if (!loggedIn) return;

        executorService.execute(() -> {
            try {
                byte[] fileContent = Files.readAllBytes(file.toPath());
                String encodedContent = Base64.getEncoder().encodeToString(fileContent);
                String mimeType = Files.probeContentType(file.toPath());
                if (mimeType == null) {
                    mimeType = "application/octet-stream";
                }

                Map<String, String> msg = new HashMap<>();
                msg.put("Command", "upload");
                msg.put("Name", file.getName());
                msg.put("MimeType", mimeType);
                msg.put("Encoding", "base64");
                msg.put("Content", encodedContent);
                MessageParser.sendMessage(out, msg);
            } catch (IOException e) {
                gui.showError("Ошибка загрузки файла: " + e.getMessage());
                disconnect();
            }
        });
    }

    public void downloadFile(String fileId) {
        if (!loggedIn) return;

        executorService.execute(() -> {
            try {
                Map<String, String> msg = new HashMap<>();
                msg.put("Command", "download");
                msg.put("FileId", fileId);
                MessageParser.sendMessage(out, msg);
            } catch (Exception e) {
                gui.showError("Ошибка запроса файла: " + e.getMessage());
                disconnect();
            }
        });
    }

    private void receiveMessages() {
        try {
            while (loggedIn && !socket.isClosed()) {
                synchronized (in) {
                    Map<String, String> msg = MessageParser.readMessage(in);
                    if (msg == null) {
                        disconnect();
                        break;
                    }
                    gui.processMessage(msg);
                }
            }
        } catch (SocketTimeoutException e) {
            if (loggedIn && !socket.isClosed()) {
                executorService.execute(this::receiveMessages);
            }
        } catch (IOException e) {
            if (loggedIn) {
                gui.showError("Соединение с сервером потеряно");
                disconnect();
            }
        }
    }

    public synchronized void disconnect() {
        if (!loggedIn) return;

        loggedIn = false;
        scheduler.shutdown();
        try {
            if (out != null) {
                Map<String, String> msg = new HashMap<>();
                msg.put("Command", "logout");
                MessageParser.sendMessage(out, msg);
            }
        } catch (Exception e) {
            System.err.println("Ошибка при отправке logout: " + e.getMessage());
        }

        try {
            if (socket != null && !socket.isClosed()) {
                socket.close();
            }
        } catch (IOException e) {
            System.err.println("Ошибка при закрытии сокета: " + e.getMessage());
        }

        gui.switchToLoginPanel();
    }

    private String hash(String s) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        return Base64.getEncoder().encodeToString(md.digest(s.getBytes("UTF-8")));
    }
}