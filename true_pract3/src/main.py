"""Точка входа CLI-приложения ассемблера."""

import argparse
import sys
from src.assembler import (
    read_asm_file, translate_to_ir, format_ir_output, AsmError
)

DEFAULT_OUTPUT = "out.bin"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ассемблер УВМ")
    parser.add_argument("-i", "--input", required=True, help="Путь к JSON файлу")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="Путь к бинарному файлу")
    parser.add_argument("-t", "--test", action="store_true", help="Режим тестирования")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    
    try:
        source_commands = read_asm_file(args.input)
        ir = translate_to_ir(source_commands)
        
        if args.test:
            print("=== Режим тестирования (Промежуточное представление) ===")
            print(format_ir_output(ir))
            
        print(f"\nУспешно ассемблировано команд: {len(ir)}")
        print(f"Выходной файл: {args.output}")
        
    except AsmError as exc:
        print(f"Ошибка ассемблирования: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()