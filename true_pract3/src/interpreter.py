import csv

OP_LOAD_CONST = 26
OP_READ_MEM = 28
OP_WRITE_MEM = 19
OP_AND = 1

MEM_SIZE = 256


def decode_load_const(code: bytes, pc: int) -> tuple[dict, int]:
    val = int.from_bytes(code[pc:pc+5], byteorder="little")
    a = val & 0x1F
    b = (val >> 5) & 0x07
    c = (val >> 8) & 0x1FFFFFF
    return {"op": "load_const", "A": a, "B": b, "C": c}, 5


def decode_read_mem(val: int) -> dict:
    a = val & 0x1F
    b = (val >> 5) & 0x07
    c = (val >> 8) & 0x1F
    d = (val >> 13) & 0x07
    return {"op": "read_mem", "A": a, "B": b, "C": c, "D": d}


def decode_standard(val: int, op_name: str) -> dict:
    a = val & 0x1F
    b = (val >> 5) & 0x07
    c = (val >> 8) & 0x07
    return {"op": op_name, "A": a, "B": b, "C": c}


def decode_command(code: bytes, pc: int) -> tuple[dict, int]:
    opcode = code[pc] & 0x1F

    if opcode == OP_LOAD_CONST:
        return decode_load_const(code, pc)
    elif opcode == OP_READ_MEM:
        val = int.from_bytes(code[pc:pc+2], byteorder="little")
        return decode_read_mem(val), 2
    elif opcode == OP_WRITE_MEM:
        val = int.from_bytes(code[pc:pc+2], byteorder="little")
        return decode_standard(val, "write_mem"), 2
    elif opcode == OP_AND:
        val = int.from_bytes(code[pc:pc+2], byteorder="little")
        return decode_standard(val, "and_op"), 2
    else:
        raise ValueError(f"Неизвестный опкод: {opcode}")


def execute_cmd(cmd: dict, memory: list[int]) -> None:
    op = cmd["op"]
    if op == "load_const":
        memory[cmd["B"]] = cmd["C"]
    elif op == "read_mem":
        addr = memory[cmd["D"]] + cmd["C"]
        memory[cmd["B"]] = memory[addr]
    elif op == "write_mem":
        memory[memory[cmd["C"]]] = memory[cmd["B"]]
    elif op == "and_op":
        memory[cmd["C"]] = memory[cmd["C"]] & memory[cmd["B"]]
    else:
        raise ValueError(f"Неизвестная команда: {op}")


def run_program(code: bytes) -> list[int]:
    memory = [0] * MEM_SIZE
    pc = 0
    while pc < len(code):
        cmd, size = decode_command(code, pc)
        execute_cmd(cmd, memory)
        pc += size
    return memory


def dump_memory_to_csv(
        memory: list[int], start: int, end: int, path: str
        ) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Address", "Value"])
        for i in range(start, end + 1):
            writer.writerow([i, memory[i]])