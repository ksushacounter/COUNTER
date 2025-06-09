package org.example.view;

import org.example.controller.PlayerController;

import java.io.IOException;

public interface View{

    void render() throws IOException;

    void KeyListener(PlayerController playerController);
}
