package org.example.view;

import javafx.animation.ScaleTransition;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.image.ImageView;
import javafx.stage.Stage;
import javafx.util.Duration;
import org.example.Main;
import org.example.model.Listener;
import org.example.model.ObjectsState;

import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;
import java.io.IOException;
import java.io.InputStream;

public class GameOverView implements Listener {
    private final int maxPrizes = 10;
    private final ObjectsState objectsState;
    ImageView logoImage;

    public GameOverView(ObjectsState objectsState){
        this.objectsState = objectsState;
    }

    public void show() {
        Platform.runLater(() -> {
            Label label;
            Stage stage = new Stage();
            stage.setTitle("Game Over");
            if (objectsState.getPlayer().getPoints() >= maxPrizes) {
                label = new Label("Вы выиграли!!!");
                label.setStyle("-fx-font-size: 18px; -fx-font-weight: bold; -fx-text-fill: red;");
            } else {
                label = new Label("Вы проиграли!");
                label.setStyle("-fx-font-size: 18px; -fx-font-weight: bold; -fx-text-fill: red;");
            }

            Button exitButton = new Button("Выйти");
            exitButton.setStyle("-fx-font-size: 14px; -fx-background-color: #ff4d4d;");
            exitButton.setOnAction(e -> {
                stage.close();
                System.exit(0);
            });


            Button restartButton = getButton(stage);
            try (InputStream inputStream = GameOverView.class.getResourceAsStream("/image/dominic.jpg")){
                javafx.scene.image.Image image = new javafx.scene.image.Image(inputStream);
                logoImage = new ImageView(image);
                logoImage.setFitWidth(250);
                logoImage.setFitHeight(100);
            }
            catch (IOException e) {
                e.printStackTrace();
            }

            VBox vbox = new VBox(20, logoImage, label, restartButton, exitButton);
            vbox.setStyle("-fx-padding: 20; -fx-alignment: center;");

            ScaleTransition scaleTransition = new ScaleTransition(Duration.seconds(0.5), vbox);
            scaleTransition.setFromX(0);
            scaleTransition.setFromY(0);
            scaleTransition.setToX(1);
            scaleTransition.setToY(1);
            scaleTransition.play();

            Scene scene = new Scene(vbox, 300, 250);
            scene.setFill(Color.LIGHTGRAY);

            stage.setScene(scene);
            stage.show();
        });
    }

    private static Button getButton(Stage stage) {
        Button restartButton = new Button("Начать заново");
        restartButton.setStyle("-fx-font-size: 14px; -fx-background-color: #4CAF50; -fx-text-fill: white;");
        restartButton.setOnAction(e -> {
            stage.close();
            try {
                Main.restartGame();
            } catch (Exception ex) {
                throw new RuntimeException(ex);
            }

        });
        return restartButton;
    }

    @Override
    public void modelChanged() throws IOException {
        if(objectsState.isGameOver()){
            this.show();
        }
    }
}
