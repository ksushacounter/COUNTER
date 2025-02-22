package ru.nsu.garkusha.topic01.task3.model;

public class Discipline {
    public String name;
    public int mark;

    public Discipline(String name, int mark){
        this.name = name;
        this.mark = mark;
    }

    @Override
    public String toString() {
        return "Discipline: " + name + "mark: " + mark;
    }

}
