
import json
from typing import Any

FIELD_SIZES = {
    "load_const": {"A": 5, "B": 3, "C": 25},
    "read_mem":   {"A": 5, "B": 3, "C": 5, "D": 3},
    "write_mem":  {"A": 5, "B": 3, "C": 3},
    "and_op":     {"A": 5, "B": 3, "C": 3},
}

COMMAND_SIZES = {
    "load_const": 5,
    "read_mem":   2,
    "write_mem":  2,
    "and_op":     2,
}

FIELD_SHIFTS = {"A": 0, "B": 5, "C": 8, "D": 13}


class AsmError(Exception):
    None


def read_asm_file(filepath: str) -> list[dict[str, Any]]:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise AsmError(f"Файл не найден: {filepath}") from exc
    except json.JSONDecodeError as exc:
        raise AsmError(f"Ошибка парсинга JSON: {exc}") from exc

    if not isinstance(data, list):
        raise AsmError("Корневой элемент JSON должен быть массивом.")
    return data


def _check_field(cmd: dict, field: str, bits: int) -> None:
    value = cmd.get(field)
    if value is None:
        raise AsmError(f"Отсутствует поле {field}")
    if not isinstance(value, int):
        raise AsmError(f"Поле {field} должно быть целым числом")

    max_val = (1 << bits) - 1
    if value < 0 or value > max_val:
        raise AsmError(
            f"Значение {field}={value} не влезает в {bits} бит "
            f"(макс {max_val})"
        )


def validate_command(cmd: dict[str, Any]) -> None:
    op = cmd.get("op")
    if op not in FIELD_SIZES:
        raise AsmError(f"Неизвестная операция: {op}")

    for field, bits in FIELD_SIZES[op].items():
        _check_field(cmd, field, bits)


def translate_to_ir(
    commands: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    ir = []
    for idx, cmd in enumerate(commands):
        try:
            validate_command(cmd)
            op = cmd["op"]
            ir.append({
                "op": op,
                "size": COMMAND_SIZES[op],
                "fields": {
                    k: cmd[k] for k in FIELD_SIZES[op]
                },
            })
        except AsmError as exc:
            raise AsmError(
                f"Ошибка в команде {idx + 1}: {exc}"
            ) from exc
    return ir


def format_ir_output(ir: list[dict[str, Any]]) -> str:
    lines = []
    for idx, cmd in enumerate(ir):
        fields = ", ".join(
            f"{k}={v}" for k, v in cmd["fields"].items()
        )
        line = (
            f"Cmd {idx + 1} ({cmd['op']}, "
            f"{cmd['size']}b): {fields}"
        )
        lines.append(line)
    return "\n".join(lines)


def pack_command(cmd: dict[str, Any]) -> bytes:
    op = cmd["op"]
    fields = cmd["fields"]

    value = 0
    for field_name, field_value in fields.items():
        shift = FIELD_SHIFTS[field_name]
        value |= (field_value << shift)

    size = COMMAND_SIZES[op]
    return value.to_bytes(size, byteorder="little")


def generate_machine_code(
    ir: list[dict[str, Any]]
) -> bytes:
    machine_code = bytearray()
    for cmd in ir:
        machine_code.extend(pack_command(cmd))
    return bytes(machine_code)


def format_bytes_output(machine_code: bytes) -> str:

    hex_bytes = [f"0x{b:02X}" for b in machine_code]
    return ", ".join(hex_bytes)