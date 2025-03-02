package org.example.commands;


import org.example.context.Context;

public interface Command {
    public void operation(Context context);
}
