package org.example.context;

import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

public class Context {
    private Stack<Double> stack;
    private Character defineName = '0';
    private Map<Character, Double> defines= new HashMap<>();

    public Context(){
        this.stack = new Stack<Double>();
    }

    public Stack<Double> getStack(){
        return stack;
    }

    public void addDefineName(char arg){
        defineName = arg;
    }
    public Character takeDefineName(){
        return defineName;
    }
//😘
    public void newDefine(Character name, Double num){
        defines.put(name,num);
    }
    public Double getVal(Character name){
        return defines.get(name);
    }
    public Map<Character, Double> getDefines(){
        return defines;
    }

}
