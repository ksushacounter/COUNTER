package org.example.view;

import javafx.animation.ScaleTransition;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.stage.Stage;
import javafx.util.Duration;
import org.example.model.Main;

import javax.print.attribute.standard.Media;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;
import java.io.IOException;

public class GameOverView {
    public static void show() {
        Platform.runLater(() -> {
            Stage stage = new Stage();
            stage.setTitle("Game Over");

            Label label = new Label("Игра окончена!");
            label.setStyle("-fx-font-size: 18px; -fx-font-weight: bold; -fx-text-fill: red;");

            Button exitButton = new Button("Выйти");
            exitButton.setStyle("-fx-font-size: 14px; -fx-background-color: #ff4d4d;");
            exitButton.setOnAction(e -> {
                stage.close();
                System.exit(0);
            });


            Button restartButton = new Button("Начать заново");
            restartButton.setStyle("-fx-font-size: 14px; -fx-background-color: #4CAF50; -fx-text-fill: white;");
            restartButton.setOnAction(e -> {
                stage.close();
                try {
                    Main.restartGame();
                } catch (UnsupportedAudioFileException ex) {
                    throw new RuntimeException(ex);
                } catch (LineUnavailableException ex) {
                    throw new RuntimeException(ex);
                } catch (IOException ex) {
                    throw new RuntimeException(ex);
                }

            });

            ImageView logoImage = new ImageView(new Image("file:C:/Users/garku/IdeaProjects/lab3/dominic.jpg"));
            logoImage.setFitWidth(250);
            logoImage.setFitHeight(100);

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
}
