package ru.nsu.garkusha.topic04.task4.module;

import java.util.function.IntFunction;

public class MakeConvert {
    enum Mode {
        ARABIC(),
        ROMAN();

        private final Converter<Number> converter;

        Mode(ConvertToString converter) {
            this.converter = converter;
        }

        public String convert(Number num) {
            return converter.convert(num);
        }
}
