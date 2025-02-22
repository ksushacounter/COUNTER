package ru.nsu.garkusha.topic01.task3.model;

import java.util.ArrayList;
import java.util.List;

public class Student {
    public String name;
    public String surname;
    public int groupNumber;
    public List<Discipline> disciplines;

    public Student (String name, String surname, int number, List<Discipline> disciplines){
        this.name = name;
        this.surname = surname;
        this.groupNumber = number;
        this.disciplines = disciplines;
    }

    @Override
    public String toString() {
        return name + " " + surname + " group: " + groupNumber;
    }

//    public boolean equals(Object obj){
//        if(this == obj){
//            return true;
//        }
//        if(obj == null || this.getClass() != obj.getClass()){
//            return false;
//        }
//
//        Student Sobj = (Student) obj;
//        if(this.name != Sobj.name || this.surname != Sobj.surname){
//            return false;
//        }
//
//        return false;
//    }
    public void printSortedGrades() {
        disciplines.sort((d1, d2) -> Double.compare(d2.mark, d1.mark));
        System.out.println(this);
        for (Discipline discipline : disciplines) {
            System.out.println(discipline);
        }
    }

}
