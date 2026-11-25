import argparse
import sys
from src.assembler import (
    read_asm_file, translate_to_ir, format_ir_output, 
    generate_machine_code, format_bytes_output, AsmError
)

DEFAULT_OUTPUT = "out.bin"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ассемблер УВМ")
    parser.add_argument("-i", "--input", required=True, help="Путь к JSON файлу")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="Путь к bin файлу")
    parser.add_argument("-t", "--test", action="store_true", help="Режим тестирования")
    return parser.parse_args()


def save_binary_file(filepath: str, data: bytes) -> None:
    with open(filepath, "wb") as file:
        file.write(data)


def main() -> None:
    args = parse_args()
    
    try:
        source_commands = read_asm_file(args.input)
        ir = translate_to_ir(source_commands)
        machine_code = generate_machine_code(ir)
        
        save_binary_file(args.output, machine_code)
        
        if args.test:
            print("=== Тестовый режим (Байтовый формат) ===")
            print(format_bytes_output(machine_code))
            print("========================================")
            
        print(f"Успешно ассемблировано команд: {len(ir)}")
        print(f"Выходной файл: {args.output}")
        
    except AsmError as exc:
        print(f"Ошибка ассемблирования: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()