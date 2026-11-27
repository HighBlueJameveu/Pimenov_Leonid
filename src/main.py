import argparse
import sys

from src.assembler import (
    read_asm_file,
    translate_to_ir,
    format_ir_output,
    generate_machine_code,
    format_bytes_output,
    AsmError,
)
from src.interpreter import (
    run_program,
    dump_memory_to_csv,
)

DEFAULT_OUTPUT = "out.bin"
DEFAULT_DUMP = "dump.csv"
DEFAULT_START = 0
DEFAULT_END = 255


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ассемблер и интерпретатор УВМ"
    )
    parser.add_argument(
        "-i", "--input",
        help="Путь к JSON файлу",
    )
    parser.add_argument("-o", "--output",
        default=DEFAULT_OUTPUT,
        help="Путь к bin файлу",
    )
    parser.add_argument("-t", "--test",
        action="store_true",
        help="Режим тестирования",
    )
    parser.add_argument("-r", "--run",
        action="store_true",
        help="Запуск интерпретатора",
    )
    parser.add_argument("--dump",
        default=DEFAULT_DUMP,
        help="Путь к CSV дампу",
    )
    parser.add_argument("--start",
        type=int,
        default=DEFAULT_START,
        help="Начало дампа",
    )
    parser.add_argument("--end",
        type=int,
        default=DEFAULT_END,
        help="Конец дампа",
    )
    return parser.parse_args()


def save_binary_file(
    filepath: str, data: bytes
) -> None:
    with open(filepath, "wb") as file:
        file.write(data)


def run_interpreter(args: argparse.Namespace) -> None:
    try:
        with open(args.output, "rb") as f:
            code = f.read()
    except FileNotFoundError:
        print(
            f"Бинарный файл не найден: {args.output}",
            file=sys.stderr,
        )
        sys.exit(1)

    memory = run_program(code)
    dump_memory_to_csv(
        memory, args.start, args.end, args.dump
    )
    print(f"Выполнение завершено. "
          f"Дамп сохранен в {args.dump}")


def assemble(args: argparse.Namespace) -> None:
    source_commands = read_asm_file(args.input)
    ir = translate_to_ir(source_commands)
    machine_code = generate_machine_code(ir)
    save_binary_file(args.output, machine_code)

    if args.test:
        print("=== Промежуточное представление ===")
        print(format_ir_output(ir))
        print("\n=== Машинный код ===")
        print(format_bytes_output(machine_code))

    print(f"Успешно ассемблировано команд: {len(ir)}")


def main() -> None:
    args = parse_args()

    if args.run:
        run_interpreter(args)
        return

    if not args.input:
        print(
            "Ошибка: укажите -i для ассемблирования",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        assemble(args)
    except AsmError as exc:
        print(f"Ошибка ассемблирования: {exc}",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()