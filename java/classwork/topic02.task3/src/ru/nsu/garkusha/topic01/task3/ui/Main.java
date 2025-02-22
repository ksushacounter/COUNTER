package ru.nsu.garkusha.topic01.task3.ui;

import ru.nsu.garkusha.topic01.task3.model.Discipline;
import ru.nsu.garkusha.topic01.task3.model.RandomGenerator;
import ru.nsu.garkusha.topic01.task3.model.Student;

import java.util.*;

public class Main {
    public static void main(String[] args) {
        RandomGenerator generator = new RandomGenerator(20);
        long studentCount = generator.getNumber();
        List<Student> Students = new ArrayList<Student>();

        String[] names = {"Sasha", "Petya", "Vasya"};
        String[] surnames = {"Petrov", "Sidorov", "Ivanov"};
        String[] Discipline = {"Math", "EVM", "OOP", "Music", "Python"};

        Random random = new Random();

        for(int i = 0; i < studentCount; i++){
            String randomName = names[(int)(Math.random() * names.length)];
            String randomSurname = surnames[(int)(Math.random() * surnames.length)];
            int randomGroup = (int)(Math.random() * 10 + 1);
            int disciplinesCount = (int)(Math.random() * 5 + 1);
            List<Discipline> disciplines = new ArrayList<>();
            for(int j = 0; j < disciplinesCount; j++){
                String randomDiscipline = Discipline[(int)(Math.random() * Discipline.length)];
                int randomMark = (int)(Math.random() * 5 + 1);
                Discipline discipline = new Discipline(randomDiscipline, randomMark);
                disciplines.add(discipline);
            }
            Student student = new Student(randomName, randomSurname, randomGroup, disciplines);
            student.printSortedGrades();
            Students.add(student);
        }
    }
}