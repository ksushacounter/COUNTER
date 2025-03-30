package org.example.view;

import org.example.model.GuessChecker;
import org.example.model.NumberGenerator;

import javax.swing.*;

class Main {
    public static void main(String[] args) {
        NumberGenerator generator = new NumberGenerator();
        String numbers = generator.numberGeneration();
        int bulls = 0;

        while(true) {
            String guess = JOptionPane.showInputDialog("Введите вашу догадку:");
            GuessChecker Checker = new GuessChecker();
            Checker.checker(guess, numbers);
            bulls = Checker.getBulls();

            if(bulls != 4) {
                JOptionPane.showMessageDialog(null, "вы не угадали!:(\n" + "коров: " + Checker.getCows() + " быков: " + Checker.getBulls());
                JOptionPane.showMessageDialog(null, "догадка: "  + guess + "\n Было загадано: " + numbers);
            }
            else{
                break;
            }

        }
        JOptionPane.showMessageDialog(null, "Вы угадали:)");
    }
}