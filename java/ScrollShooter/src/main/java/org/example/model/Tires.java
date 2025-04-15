package org.example.model;

import org.example.view.Rendering;
import java.util.List;

import static java.lang.Thread.sleep;

public class Tires implements Runnable{
    private Rendering view;
    private List<Tire> tires;

    Tires(Rendering view, List<Tire> tires){
        this.view = view;
        this.tires = tires;
    }

    @Override
    public void run() {
        while (!Thread.interrupted()) {
            for(Tire tire : tires){
                tire.moveDown();
            }

            Tire tire = new Tire(20, 10);
            try {
                sleep(1000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            Tire tire2 = new Tire(100, 10);
            tires.add(tire);
            tires.add(tire2);
            view.repaint();
            try {
                sleep(1000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }
}
