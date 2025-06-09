package ru.nsu.garkusha;

import java.util.Locale;
import java.util.concurrent.atomic.*;

public class TickerStats {
    private final LongAdder count = new LongAdder();
    private final DoubleAdder sum = new DoubleAdder();
    private final AtomicReference<Double> min = new AtomicReference<>(Double.MAX_VALUE);
    private final AtomicReference<Double> max = new AtomicReference<>(Double.MIN_VALUE);
    private final AtomicReference<Double> last = new AtomicReference<>(0.0);
    private final AtomicLong lastTime = new AtomicLong(Long.MIN_VALUE);

    public void update(double price, long time) {
        count.increment();
        sum.add(price);
        min.getAndUpdate(v -> Math.min(v, price));
        max.getAndUpdate(v -> Math.max(v, price));
        lastTime.getAndUpdate(old -> Math.max(old, time));
        last.updateAndGet(prev -> (time >= lastTime.get()) ? price : prev);
        synchronized(this) {
            min.getAndUpdate(v -> Math.min(v, price));
        }
    }

    public String getSummary() {
        long c = count.sum();
        double avg = c > 0 ? sum.sum() / c : 0.0;
        return String.format(Locale.US, "AVG: %.2f | MIN: %.2f | MAX: %.2f | LAST: %.2f", avg, min.get(), max.get(), last.get());
    }
}
