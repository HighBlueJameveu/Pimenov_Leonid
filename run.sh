#!/usr/bin/env bash

if [ $# -lt 1 ]; then
    echo "Использование: ./run.sh <файл.json>"
    exit 1
fi

INPUT_JSON="$1"
OUTPUT_BIN="out.bin"
DUMP_CSV="dump.csv"

echo "Ассемблирование $INPUT_JSON..."
PYTHONPATH=. python3 src/main.py -i "$INPUT_JSON" -o "$OUTPUT_BIN"

if [ $? -ne 0 ]; then
    echo "Ошибка ассемблирования"
    exit 1
fi

echo "Бинарный файл создан: $OUTPUT_BIN"

echo "Выполнение программы..."
PYTHONPATH=. python3 src/main.py -r -o "$OUTPUT_BIN" --dump "$DUMP_CSV"

if [ $? -eq 0 ]; then
    echo "Выполнение завершено. Дамп сохранён в $DUMP_CSV"
else
    echo "Ошибка выполнения"
    exit 1
fi