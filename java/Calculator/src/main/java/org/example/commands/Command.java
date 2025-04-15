package org.example.commands;


import org.example.context.Contexts;

public interface Command {
    void operation(Contexts context);
}
