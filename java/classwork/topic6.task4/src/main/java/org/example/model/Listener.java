package org.example.model;

import org.example.view.View;

public class Listener {
    public void change(View view, String print){
        view.rendering(print);
    }
}
