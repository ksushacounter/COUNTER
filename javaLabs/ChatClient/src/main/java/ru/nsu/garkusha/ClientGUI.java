package ru.nsu.garkusha;

import javax.swing.*;
import javax.swing.event.MouseInputAdapter;
import javax.swing.text.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

public class ClientGUI {
    private final Client client;
    private JFrame frame;
    private JPanel loginPanel;
    private JPanel chatPanel;
    private JTextField ipField;
    private JTextField portField;
    private JTextField loginField;
    private JPasswordField passwordField;
    private JTextPane chatArea;
    private JTextField messageField;
    private DefaultListModel<String> userListModel;
    private JList<String> userList;
    private StyledDocument doc;
    private SimpleAttributeSet defaultStyle;
    private SimpleAttributeSet linkStyle;

    public ClientGUI() {
        this.client = new Client(this);
        createGUI();
    }

    private void createGUI() {
        frame = new JFrame("Чат-клиент");
        frame.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        frame.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                client.disconnect();
                System.exit(0);
            }
        });
        frame.setSize(600, 400);
        frame.setLocationRelativeTo(null);
        frame.setLayout(new BorderLayout());

        createLoginPanel();
        createChatPanel();

        frame.add(loginPanel, BorderLayout.CENTER);
        frame.setVisible(true);
    }

    private void createLoginPanel() {
        loginPanel = new JPanel(new GridBagLayout());
        loginPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        gbc.gridx = 0;
        gbc.gridy = 0;
        loginPanel.add(new JLabel("IP-адрес:"), gbc);
        gbc.gridx = 1;
        ipField = new JTextField("localhost", 15);
        loginPanel.add(ipField, gbc);

        gbc.gridx = 0;
        gbc.gridy = 1;
        loginPanel.add(new JLabel("Порт:"), gbc);
        gbc.gridx = 1;
        portField = new JTextField("12345", 15);
        loginPanel.add(portField, gbc);

        gbc.gridx = 0;
        gbc.gridy = 2;
        loginPanel.add(new JLabel("Имя пользователя:"), gbc);
        gbc.gridx = 1;
        loginField = new JTextField(15);
        loginPanel.add(loginField, gbc);

        gbc.gridx = 0;
        gbc.gridy = 3;
        loginPanel.add(new JLabel("Пароль:"), gbc);
        gbc.gridx = 1;
        passwordField = new JPasswordField(15);
        loginPanel.add(passwordField, gbc);

        gbc.gridx = 0;
        gbc.gridy = 4;
        gbc.gridwidth = 2;
        JButton loginButton = new JButton("Войти");
        loginButton.addActionListener(e -> login());
        loginPanel.add(loginButton, gbc);

        loginField.addActionListener(e -> login());
        passwordField.addActionListener(e -> login());
        ipField.addActionListener(e -> login());
        portField.addActionListener(e -> login());

        loginField.requestFocus();
    }

    private void createChatPanel() {
        chatPanel = new JPanel(new BorderLayout(5, 5));
        chatPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        chatArea = new JTextPane();
        chatArea.setEditable(false);
        doc = chatArea.getStyledDocument();
        defaultStyle = new SimpleAttributeSet();
        StyleConstants.setFontFamily(defaultStyle, "Monospaced");
        StyleConstants.setFontSize(defaultStyle, 14);

        linkStyle = new SimpleAttributeSet();
        StyleConstants.setForeground(linkStyle, Color.BLUE);
        StyleConstants.setUnderline(linkStyle, true);
        StyleConstants.setFontFamily(linkStyle, "Monospaced");
        StyleConstants.setFontSize(linkStyle, 14);

        chatArea.addMouseListener(new MouseInputAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                try {
                    int pos = chatArea.viewToModel2D(e.getPoint());
                    Element elem = doc.getCharacterElement(pos);
                    AttributeSet as = elem.getAttributes();
                    String fileId = (String) as.getAttribute("fileId");
                    if (fileId != null) {
                        client.downloadFile(fileId);
                        System.out.println("Requesting download for FileId: " + fileId);
                    }
                } catch (Exception ex) {
                    System.err.println("Error in mouse click: " + ex.getMessage());
                }
            }
        });
        chatArea.setCursor(new Cursor(Cursor.HAND_CURSOR));
        JScrollPane chatScroll = new JScrollPane(chatArea);
        chatPanel.add(chatScroll, BorderLayout.CENTER);

        JPanel bottomPanel = new JPanel(new BorderLayout(5, 0));
        messageField = new JTextField();
        messageField.addActionListener(e -> sendMessage());
        bottomPanel.add(messageField, BorderLayout.CENTER);

        JButton sendButton = new JButton("Отправить");
        sendButton.addActionListener(e -> sendMessage());
        bottomPanel.add(sendButton, BorderLayout.EAST);

        JButton uploadButton = new JButton("Загрузить файл");
        uploadButton.addActionListener(e -> uploadFile());
        bottomPanel.add(uploadButton, BorderLayout.WEST);

        JButton logoutButton = new JButton("Выйти");
        logoutButton.addActionListener(e -> client.disconnect());
        bottomPanel.add(logoutButton, BorderLayout.NORTH);

        chatPanel.add(bottomPanel, BorderLayout.SOUTH);

        userListModel = new DefaultListModel<>();
        userList = new JList<>(userListModel);
        JScrollPane userScroll = new JScrollPane(userList);
        userScroll.setPreferredSize(new Dimension(120, 0));
        JPanel rightPanel = new JPanel(new BorderLayout());
        rightPanel.add(new JLabel("Пользователи", SwingConstants.CENTER), BorderLayout.NORTH);
        rightPanel.add(userScroll, BorderLayout.CENTER);
        chatPanel.add(rightPanel, BorderLayout.EAST);
    }

    private void login() {
        String ip = ipField.getText().trim();
        String portStr = portField.getText().trim();
        int port;
        try {
            port = Integer.parseInt(portStr);
        } catch (NumberFormatException e) {
            showError("Неверный формат порта");
            return;
        }
        String username = loginField.getText().trim();
        String password = new String(passwordField.getPassword()).trim();
        client.login(ip, port, username, password);
    }

    private void sendMessage() {
        String text = messageField.getText().trim();
        if (!text.isEmpty()) {
            client.sendMessage(text);
        }
    }

    private void uploadFile() {
        JFileChooser fileChooser = new JFileChooser();
        if (fileChooser.showOpenDialog(frame) == JFileChooser.APPROVE_OPTION) {
            File file = fileChooser.getSelectedFile();
            client.uploadFile(file);
        }
    }

    public void switchToChatPanel() {
        SwingUtilities.invokeLater(() -> {
            frame.remove(loginPanel);
            frame.add(chatPanel, BorderLayout.CENTER);
            frame.revalidate();
            frame.repaint();
            messageField.requestFocus();
        });
    }

    public void switchToLoginPanel() {
        SwingUtilities.invokeLater(() -> {
            frame.remove(chatPanel);
            frame.add(loginPanel, BorderLayout.CENTER);
            ipField.setText("localhost");
            portField.setText("12345");
            loginField.setText("");
            passwordField.setText("");
            try {
                doc.remove(0, doc.getLength());
            } catch (BadLocationException e) {
                e.printStackTrace();
            }
            userListModel.clear();
            frame.revalidate();
            frame.repaint();
            loginField.requestFocus();
        });
    }

    public void showError(String message) {
        SwingUtilities.invokeLater(() ->
                JOptionPane.showMessageDialog(frame, message, "Ошибка", JOptionPane.ERROR_MESSAGE));
    }

    public void clearMessageField() {
        SwingUtilities.invokeLater(() -> messageField.setText(""));
    }

    public void processMessage(Map<String, String> msg) {
        String status = msg.get("status");
        if (status != null) {
            if ("Success".equalsIgnoreCase(status) && msg.containsKey("usercount")) {
                userListModel.clear();
                int count = Integer.parseInt(msg.get("usercount"));
                for (int i = 1; i <= count; i++) {
                    String user = msg.get("username" + i);
                    if (user != null) {
                        userListModel.addElement(user);
                    }
                }
            } else if ("Success".equalsIgnoreCase(status) && msg.containsKey("fileid")) {
                if (msg.containsKey("content")) {
                    saveFile(msg);
                }
            } else if ("Error".equalsIgnoreCase(status)) {
                String error = msg.get("message");
                showError(error != null ? error : "Неизвестная ошибка");
                if ("Login required".equals(error) || "Wrong password".equals(error)) {
                    client.disconnect();
                }
            }
            return;
        }

        String event = msg.get("event");
        if (event != null) {
            try {
                switch (event.toLowerCase()) {
                    case "message":
                        String from = msg.get("from");
                        String message = msg.get("message");
                        if (from != null && message != null) {
                            doc.insertString(doc.getLength(), from + ": " + message + "\n", defaultStyle);
                        }
                        break;
                    case "userlogin":
                        String newUser = msg.get("username");
                        if (newUser != null && !userListModel.contains(newUser)) {
                            userListModel.addElement(newUser);
                            doc.insertString(doc.getLength(), "Пользователь " + newUser + " вошел в чат\n", defaultStyle);
                        }
                        break;
                    case "userlogout":
                        String oldUser = msg.get("username");
                        if (oldUser != null) {
                            userListModel.removeElement(oldUser);
                            doc.insertString(doc.getLength(), "Пользователь " + oldUser + " вышел из чата\n", defaultStyle);
                        }
                        break;
                    case "file":
                        String fileFrom = msg.get("from");
                        String fileName = msg.get("name");
                        String fileSize = msg.get("size");
                        String fileId = msg.get("fileid");
                        String mimeType = msg.get("mimetype");
                        if (fileFrom != null && fileName != null && fileSize != null && fileId != null) {
                            String prefix = String.format("Пользователь %s отправил файл [File: %s, Size: %s bytes, ",
                                    fileFrom, fileName, fileSize);
                            doc.insertString(doc.getLength(), prefix, defaultStyle);
                            SimpleAttributeSet linkAttrs = new SimpleAttributeSet(linkStyle);
                            linkAttrs.addAttribute("fileId", fileId);
                            doc.insertString(doc.getLength(), fileName, linkAttrs);
                            doc.insertString(doc.getLength(), "]\n", defaultStyle);
                            System.out.println("File link added: " + fileName + " (FileId: " + fileId + ")");
                        }
                        break;
                }
            } catch (BadLocationException e) {
                System.err.println("BadLocationException in processMessage: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }

    private void saveFile(Map<String, String> msg) {
        String fileName = msg.get("name");
        String content = msg.get("content");
        String mimeType = msg.get("mimetype");
        String fileId = msg.get("fileid");

        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setSelectedFile(new File(fileName));
        if (fileChooser.showSaveDialog(frame) == JFileChooser.APPROVE_OPTION) {
            File file = fileChooser.getSelectedFile();
            try {
                byte[] fileContent = Base64.getDecoder().decode(content);
                Files.write(file.toPath(), fileContent);
                showError("Файл успешно сохранен: " + file.getAbsolutePath());
            } catch (IOException e) {
                showError("Ошибка сохранения файла: " + e.getMessage());
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(ClientGUI::new);
    }
}