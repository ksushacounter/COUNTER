package org.example.model;

import org.example.view.View;

import java.util.ArrayList;
import java.util.List;

public class model {
    private List<Listener> listeners = new ArrayList<>();
    private View view = new View();


    public void addListener(Listener listener) {
        listeners.add(listener);
    }
    public void hasChange(){
        for(Listener listener : listeners){
            listener.change(view, );
        }
    }
}
