package org.example.model;

import javax.sound.sampled.*;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public class Audio {
    public Clip clip;
    private AudioInputStream  family;

    public Audio() throws UnsupportedAudioFileException, IOException, LineUnavailableException {
        try (InputStream audioStream = getClass().getResourceAsStream("/music/Teriyaki_Boyz_-_Tokyo_Drift_Fast_Furious.wav")) {
            if (audioStream == null) {
                throw new RuntimeException("Аудиофайл не найден в ресурсах!");
            }
            Path tempFile = Files.createTempFile("temp-audio-", ".wav");
            Files.copy(audioStream, tempFile, StandardCopyOption.REPLACE_EXISTING);
            tempFile.toFile().deleteOnExit();

            AudioInputStream audio = AudioSystem.getAudioInputStream(tempFile.toFile());
            clip = AudioSystem.getClip();
            clip.open(audio);
            clip.start();

        } catch (IOException | UnsupportedAudioFileException | LineUnavailableException e) {
            e.printStackTrace();
        }
        try (InputStream audioStream = getClass().getResourceAsStream("/music/dominik-toretto-semya-jeto-glavnoe.wav")) {
            if (audioStream == null) {
                throw new RuntimeException("Аудиофайл не найден в ресурсах!");
            }
            Path tempFile = Files.createTempFile("temp-audio-", ".wav");
            Files.copy(audioStream, tempFile, StandardCopyOption.REPLACE_EXISTING);
            tempFile.toFile().deleteOnExit();
            family = AudioSystem.getAudioInputStream(tempFile.toFile());

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void stopAndClose() {
        if (clip != null) {
            clip.stop();
            clip.close();
        }
    }

    public void GameOver() {
        stopAndClose();
        try {
            clip = AudioSystem.getClip();
            clip.open(family);
            clip.start();
        } catch (IOException | LineUnavailableException ex) {
            throw new RuntimeException(ex);
        }
    }
}
