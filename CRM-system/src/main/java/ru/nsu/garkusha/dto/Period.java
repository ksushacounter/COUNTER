package ru.nsu.garkusha.dto;

import java.time.LocalDateTime;

public class Period {
    private LocalDateTime start;
    private LocalDateTime end;
    private int count;

    public Period() {
    }

    public Period(LocalDateTime start, LocalDateTime end, int count) {
        this.start = start;
        this.end = end;
        this.count = count;
    }

    public LocalDateTime getStart() {
        return start;
    }

    public void setStart(LocalDateTime start) {
        this.start = start;
    }

    public LocalDateTime getEnd() {
        return end;
    }

    public void setEnd(LocalDateTime end) {
        this.end = end;
    }

    public int getCount() {
        return count;
    }

    public void setCount(int count) {
        this.count = count;
    }
}