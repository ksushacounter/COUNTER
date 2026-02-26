package ru.nsu.garkusha.network;

import com.google.protobuf.InvalidProtocolBufferException;
import ru.nsu.garkusha.proto.SnakesProto.GameMessage;
import ru.nsu.garkusha.proto.SnakesProto;

import javax.swing.*;
import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;


public class NetworkManager {
    private static final String MULTICAST_ADDRESS = "239.192.0.4";
//    private static final String MULTICAST_ADDRESS = "224.0.0.1";
    private static final int MULTICAST_PORT = 9192;

    private DatagramSocket unicastSocket;
    private MulticastSocket multicastSocket;
    private InetAddress multicastGroup;

    private final ConcurrentMap<InetSocketAddress, Long> lastReceivedTime;
    private final ConcurrentMap<InetSocketAddress, Long> lastSentTime;

    private ScheduledExecutorService scheduler;
    private final BlockingQueue<ReceivedMessage> messageQueue;

    private MessageListener messageListener;

    private final AtomicLong messageSequence;

    private long pingInterval;
    private long timeoutInterval;

    private volatile boolean running;

    public interface MessageListener {
        void onMessageReceived(GameMessage message, InetAddress senderAddress, int senderPort);
    }

    private static class ReceivedMessage {
        final GameMessage message;
        final InetAddress address;
        final int port;

        ReceivedMessage(GameMessage message, InetAddress address, int port) {
            this.message = message;
            this.address = address;
            this.port = port;
        }
    }

    public NetworkManager(MessageListener listener) {
        this.messageListener = listener;
        this.messageSequence = new AtomicLong(1);
        this.messageQueue = new LinkedBlockingQueue<>();
        this.lastReceivedTime = new ConcurrentHashMap<>();
        this.lastSentTime = new ConcurrentHashMap<>();
        this.running = false;
    }

    public void start(int stateDelayMs) throws IOException {
        if (running) {
            return;
        }

        this.pingInterval = stateDelayMs / 10;
        this.timeoutInterval = (long) (stateDelayMs * 0.8);

        unicastSocket = new DatagramSocket();
        unicastSocket.setSoTimeout(1000);
        InetAddress group = InetAddress.getByName(MULTICAST_ADDRESS);
        multicastSocket = new MulticastSocket(MULTICAST_PORT);
        multicastGroup = InetAddress.getByName(MULTICAST_ADDRESS);
        multicastSocket.joinGroup(new InetSocketAddress(group, MULTICAST_PORT), NetworkInterface.getByName("Беспроводная сеть"));
        multicastSocket.setSoTimeout(1000);

        scheduler = Executors.newScheduledThreadPool(4);

        running = true;

        startMessageReceiver();
        startMessageProcessor();
        startTimers();

        System.out.printf("NetworkManager started. Unicast port: %d, Multicast: %s:%d%n",
                unicastSocket.getLocalPort(), MULTICAST_ADDRESS, MULTICAST_PORT);
    }

    public void stop() {
        if (!running) {
            return;
        }

        running = false;

        if (scheduler != null) {
            scheduler.shutdown();
            try {
                scheduler.awaitTermination(2, TimeUnit.SECONDS);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        if (multicastSocket != null && multicastGroup != null) {
            try {
                multicastSocket.leaveGroup(multicastGroup);
            } catch (IOException e) {
                e.printStackTrace();
            }
            multicastSocket.close();
        }

        if (unicastSocket != null) {
            unicastSocket.close();
        }

        messageQueue.clear();
        lastReceivedTime.clear();
        lastSentTime.clear();
    }

    private void startMessageReceiver() {
        scheduler.execute(() -> {
            while (running) {
                try {
                    receiveUnicast();
                } catch (SocketTimeoutException e) {
                } catch (IOException e) {
                    if (running) {
                        e.printStackTrace();
                    }
                }
            }
        });

        scheduler.execute(() -> {
            while (running) {
                try {
                    receiveMulticast();
                } catch (SocketTimeoutException e) {
                } catch (IOException e) {
                    if (running) {
                        e.printStackTrace();
                    }
                }
            }
        });
    }

    private void receiveUnicast() throws IOException {
        byte[] buffer = new byte[65535];
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
        unicastSocket.receive(packet);

        processReceivedPacket(packet);
    }

    private void receiveMulticast() throws IOException {
        byte[] buffer = new byte[65535];
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
        multicastSocket.receive(packet);
        processReceivedPacket(packet);
    }

    private void processReceivedPacket(DatagramPacket packet) {
        try {
            byte[] data = new byte[packet.getLength()];
            System.arraycopy(packet.getData(), 0, data, 0, packet.getLength());

            GameMessage message = GameMessage.parseFrom(data);
            InetSocketAddress senderAddress = new InetSocketAddress(
                    packet.getAddress(), packet.getPort());
            lastReceivedTime.put(senderAddress, System.currentTimeMillis());

            messageQueue.put(new ReceivedMessage(message,
                    packet.getAddress(), packet.getPort()));

        } catch (InvalidProtocolBufferException e) {
            System.err.println("Invalid protobuf message received: " + e.getMessage());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } catch (Exception e) {
            System.err.println("Error processing packet: " + e.getMessage());
        }
    }

    private void startMessageProcessor() {
        scheduler.execute(() -> {
            while (running) {
                try {
                    ReceivedMessage received = messageQueue.take();

                    if (messageListener != null) {
                        SwingUtilities.invokeLater(() -> {
                            messageListener.onMessageReceived(
                                    received.message, received.address, received.port);
                        });
                    }

                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
    }


    private void startTimers() {
        scheduler.scheduleAtFixedRate(() -> {
            checkAndSendPings();
        }, pingInterval, pingInterval, TimeUnit.MILLISECONDS);

        scheduler.scheduleAtFixedRate(() -> {
            checkTimeouts();
        }, timeoutInterval / 2, timeoutInterval / 2, TimeUnit.MILLISECONDS);
    }


    private void checkAndSendPings() {
        long currentTime = System.currentTimeMillis();

        for (Map.Entry<InetSocketAddress, Long> entry : lastSentTime.entrySet()) {
            InetSocketAddress address = entry.getKey();
            long lastSent = entry.getValue();

            if (currentTime - lastSent > pingInterval) {
                sendPing(address.getAddress(), address.getPort());
            }
        }
    }


    private void checkTimeouts() {
        long currentTime = System.currentTimeMillis();
        List<InetSocketAddress> timedOut = new ArrayList<>();

        for (Map.Entry<InetSocketAddress, Long> entry : lastReceivedTime.entrySet()) {
            if (currentTime - entry.getValue() > timeoutInterval) {
                timedOut.add(entry.getKey());
            }
        }

        for (InetSocketAddress address : timedOut) {
            lastReceivedTime.remove(address);
            lastSentTime.remove(address);
            SnakesProto.GameMessage timeoutMessage = SnakesProto.GameMessage.newBuilder()
                    .setMsgSeq(-888)
                    .setPing(SnakesProto.GameMessage.PingMsg.newBuilder().build())
                    .build();
            if (messageListener != null) {
                final InetSocketAddress finalAddress = address;
                SwingUtilities.invokeLater(() -> {
                    messageListener.onMessageReceived(
                            timeoutMessage, address.getAddress(), address.getPort());
                    System.out.println("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
                });
            }
        }
    }

    public void sendUnicast(GameMessage message, InetAddress address, int port) {
        try {
            byte[] data = message.toByteArray();
            DatagramPacket packet = new DatagramPacket(data, data.length, address, port);
            unicastSocket.send(packet);

            lastSentTime.put(new InetSocketAddress(address, port), System.currentTimeMillis());

        } catch (IOException e) {
            System.err.printf("Failed to send message to %s:%d: %s%n",
                    address, port, e.getMessage());
        }
    }

    public void sendMulticast(GameMessage message) {
        try {
            byte[] data = message.toByteArray();
            DatagramPacket packet = new DatagramPacket(
                    data, data.length, multicastGroup, MULTICAST_PORT);
            unicastSocket.send(packet);

        } catch (IOException e) {
            System.err.printf("Failed to send multicast message: %s%n", e.getMessage());
        }
    }


    public void sendAck(long msgSeq, int senderId, int receiverId,
                        InetAddress address, int port) {
        GameMessage ackMessage = GameMessage.newBuilder()
                .setMsgSeq(msgSeq)
                .setSenderId(senderId)
                .setReceiverId(receiverId)
                .setAck(SnakesProto.GameMessage.AckMsg.newBuilder().build())
                .build();
        sendUnicast(ackMessage, address, port);
    }


    private void sendPing(InetAddress address, int port) {
        long seq = messageSequence.getAndIncrement();
        GameMessage pingMessage = GameMessage.newBuilder()
                .setMsgSeq(seq)
                .setPing(SnakesProto.GameMessage.PingMsg.newBuilder().build())
                .build();

        sendUnicast(pingMessage, address, port);
    }

    public GameMessage createAnnouncement(List<SnakesProto.GameAnnouncement> games) {
        long seq = messageSequence.getAndIncrement();
        return GameMessage.newBuilder()
                .setMsgSeq(seq)
                .setAnnouncement(SnakesProto.GameMessage.AnnouncementMsg.newBuilder()
                        .addAllGames(games)
                        .build())
                .build();
    }


    public GameMessage createStateMsg(SnakesProto.GameState state, int senderId) {
        long seq = messageSequence.getAndIncrement();
        return GameMessage.newBuilder()
                .setMsgSeq(seq)
                .setSenderId(senderId)
                .setState(SnakesProto.GameMessage.StateMsg.newBuilder()
                        .setState(state)
                        .build())
                .build();
    }

    public GameMessage createSteerMsg(SnakesProto.Direction direction, int senderId) {
        long seq = messageSequence.getAndIncrement();
        System.out.println("[NetworkManager] Created STEER msg: senderId=" + senderId +
                ", seq=" + seq + ", direction=" + direction);
        return GameMessage.newBuilder()
                .setMsgSeq(seq)
                .setSenderId(senderId)
                .setSteer(SnakesProto.GameMessage.SteerMsg.newBuilder()
                        .setDirection(direction)
                        .build())
                .build();
    }

    public GameMessage createJoinMsg(String playerName, String gameName,
                                     SnakesProto.NodeRole requestedRole) {
        long seq = messageSequence.getAndIncrement();
        return GameMessage.newBuilder()
                .setMsgSeq(seq)
                .setJoin(SnakesProto.GameMessage.JoinMsg.newBuilder()
                        .setPlayerName(playerName)
                        .setGameName(gameName)
                        .setRequestedRole(requestedRole)
                        .build())
                .build();
    }

    public int getLocalPort() {
        return unicastSocket != null ? unicastSocket.getLocalPort() : -1;
    }

    public boolean isRunning() {
        return running;
    }
}