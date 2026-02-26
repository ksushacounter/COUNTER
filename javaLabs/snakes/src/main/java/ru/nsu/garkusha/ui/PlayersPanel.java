package ru.nsu.garkusha.ui;

import ru.nsu.garkusha.game.GamePlayer;
import ru.nsu.garkusha.proto.SnakesProto;
import javax.swing.*;
import javax.swing.table.*;
import java.awt.*;
import java.util.List;


public class PlayersPanel extends JPanel {
    private JTable playersTable;
    private PlayersTableModel tableModel;

    public PlayersPanel() {
        setLayout(new BorderLayout());
        setBorder(BorderFactory.createTitledBorder("Players"));

        initTable();

        JPanel controlPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));

        JButton refreshButton = new JButton("Refresh");
        refreshButton.addActionListener(e -> refreshTable());

        controlPanel.add(refreshButton);

        add(controlPanel, BorderLayout.NORTH);

        setPreferredSize(new Dimension(250, 400));
    }

    private void initTable() {
        tableModel = new PlayersTableModel();
        playersTable = new JTable(tableModel);

        playersTable.setRowHeight(25);
        playersTable.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        playersTable.setShowGrid(true);
        playersTable.setGridColor(Color.LIGHT_GRAY);

        TableColumnModel columnModel = playersTable.getColumnModel();
        columnModel.getColumn(0).setPreferredWidth(30);
        columnModel.getColumn(1).setPreferredWidth(100);
        columnModel.getColumn(2).setPreferredWidth(50);
        columnModel.getColumn(3).setPreferredWidth(70);

        DefaultTableCellRenderer centerRenderer = new DefaultTableCellRenderer();
        centerRenderer.setHorizontalAlignment(JLabel.CENTER);

        for (int i = 0; i < playersTable.getColumnCount(); i++) {
            playersTable.getColumnModel().getColumn(i).setCellRenderer(centerRenderer);
        }

        playersTable.setDefaultRenderer(Object.class, new RoleCellRenderer());

        JScrollPane scrollPane = new JScrollPane(playersTable);
        add(scrollPane, BorderLayout.CENTER);
    }


    public void updatePlayers(List<GamePlayer> players) {
        tableModel.updatePlayers(players);
    }


    private void refreshTable() {
        tableModel.fireTableDataChanged();
    }


    private static class PlayersTableModel extends AbstractTableModel {
        private List<GamePlayer> players;
        private final String[] columnNames = {"ID", "Name", "Score", "Role"};

        public PlayersTableModel() {
            players = java.util.Collections.emptyList();
        }

        public void updatePlayers(List<GamePlayer> players) {
            this.players = players;
            fireTableDataChanged();
        }

        @Override
        public int getRowCount() {
            return players.size();
        }

        @Override
        public int getColumnCount() {
            return columnNames.length;
        }

        @Override
        public String getColumnName(int column) {
            return columnNames[column];
        }

        @Override
        public Object getValueAt(int rowIndex, int columnIndex) {
            if (players == null || rowIndex >= players.size()) {
                return null;
            }

            GamePlayer player = players.get(rowIndex);

            switch (columnIndex) {
                case 0: return player.getId();
                case 1: return player.getName();
                case 2: return player.getScore();
                case 3:
                    System.out.println(getRoleString(player.getRole()) + "sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss"); return getRoleString(player.getRole());
                default: return null;
            }

        }

        @Override
        public Class<?> getColumnClass(int columnIndex) {
            switch (columnIndex) {
                case 0: return Integer.class;
                case 2: return Integer.class;
                default: return String.class;
            }
        }

        private String getRoleString(SnakesProto.NodeRole role) {
            switch (role) {
                case MASTER: return "MASTER";
                case NORMAL: return "PLAYER";
                case VIEWER: return "VIEWER";
                case DEPUTY: return "DEPUTY";
                default: return "UNKNOWN";
            }
        }
    }


    private static class RoleCellRenderer extends DefaultTableCellRenderer {
        @Override
        public Component getTableCellRendererComponent(JTable table, Object value,
                                                       boolean isSelected, boolean hasFocus, int row, int column) {
            Component c = super.getTableCellRendererComponent(table, value,
                    isSelected, hasFocus, row, column);

            if (column == 3) {
                String role = (String) value;
                if (role != null) {
                    switch (role) {
                        case "MASTER":
                            c.setBackground(new Color(220, 235, 255));
                            break;
                        case "DEPUTY":
                            c.setBackground(new Color(255, 240, 220));
                            break;
                        case "VIEWER":
                            c.setBackground(new Color(240, 240, 240));
                            break;
                        default:
                            c.setBackground(Color.WHITE);
                    }
                }
            } else {
                c.setBackground(Color.WHITE);
            }

            if (isSelected) {
                c.setBackground(table.getSelectionBackground());
                c.setForeground(table.getSelectionForeground());
            } else {
                c.setForeground(table.getForeground());
            }

            setHorizontalAlignment(JLabel.CENTER);
            return c;
        }
    }
}