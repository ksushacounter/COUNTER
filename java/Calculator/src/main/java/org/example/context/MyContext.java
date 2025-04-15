package org.example.context;

import java.util.*;

public class MyContext implements Contexts {
    private Stack<Double> stack;
    private Map<Character, Double> defines = new HashMap<>();
    private List<String> line = new ArrayList<>();

    public MyContext() {
        this.stack = new Stack<Double>();
    }

    public Stack<Double> getStack() {
        return stack;
    }

    //😘
    public void newDefine(Character name, Double num) {
        defines.put(name, num);
    }

    public Double getVal(Character name) {
        return defines.get(name);
    }

    public Map<Character, Double> getDefines() {
        return defines;
    }

    @Override
    public void addLine(List<String> newLine) {
        line = newLine;
    }

    @Override
    public List<String> getLine() {
        return line;
    }

}
