import tkinter as tk
import os
import socket
import getpass
import argparse
import sys

parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")
parser.add_argument("--vfs", type=str, default="./vfs_root", help="Путь к физическому расположению VFS")
parser.add_argument("--script", type=str, help="Путь к стартовому скрипту")
args = parser.parse_args()

# Отладочный вывод при запуске (Требование 1)
print(f"Запуск эмулятора...")
print(f"Путь к VFS - {os.path.abspath(args.vfs)}")
print(f"Путь к скрипту - {os.path.abspath(args.script) if args.script else 'Не задан'}")

try:
    username = getpass.getuser()
except Exception:
    username = "unknown_user"

try:
    hostname = socket.gethostname()
except Exception:
    hostname = "unknown_host"

window_title = f"Эмулятор - [{username}@{hostname}]"

def print_to_console(text):
    console_text.config(state=tk.NORMAL)
    console_text.insert(tk.END, text + "\n")
    console_text.see(tk.END)
    console_text.config(state=tk.DISABLED)

def execute_command(full_command):
    if not full_command:
        return True

    parts = full_command.split()
    command = parts[0]
    cmd_args = parts[1:]

    if command == "ls":
        print_to_console(f"Эмулятор: Команда 'ls' вызвана с аргументами: {cmd_args}")
        return True
    elif command == "cd":
        print_to_console(f"Эмулятор: Команда 'cd' вызвана с аргументами: {cmd_args}")
        return True
    elif command == "exit":
        print_to_console("Завершение работы эмулятора")
        root.after(500, root.destroy)
        return False
    else:
        print_to_console(f"Эмулятор: команда '{command}' не найдена")
        return False

def process_command(event=None):
    full_command = entry_command.get().strip()
    entry_command.delete(0, tk.END)
    
    if not full_command:
        return

    print_to_console(f"[{username}@{hostname}]$ {full_command}")
    execute_command(full_command)

script_lines = []
current_line_index = 0

def run_next_script_line():
    global current_line_index
    if current_line_index >= len(script_lines):
        print_to_console("Скрипт завершился")
        return

    line = script_lines[current_line_index].strip()
    current_line_index += 1

    if not line or line.startswith("#"):
        root.after(100, run_next_script_line)
        return

    print_to_console(f"[{username}@{hostname}]$ {line}")
    
    success = execute_command(line)
    
    if success:
        root.after(500, run_next_script_line)
    else:
        print_to_console("Выполнение скрипта остановлено из-за ошибки, кирдык")

def start_script_execution():
    global script_lines
    if args.script:
        try:
            with open(args.script, 'r', encoding='utf-8') as f:
                script_lines = f.readlines()
            print_to_console(f"Запуск скрипта {args.script}")
            root.after(500, run_next_script_line)
        except FileNotFoundError:
            print_to_console(f"Ошибка, '{args.script}' не найден")


root = tk.Tk()
root.title(window_title)
root.geometry("800x600")

console_text = tk.Text(root, bg="black", fg="#411dd1", font=("Consolas", 12), wrap="word")
console_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
console_text.config(state=tk.DISABLED)

input_frame = tk.Frame(root)
input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

prompt_label = tk.Label(input_frame, text=f"[{username}@{hostname}]$ ", font=("Consolas", 12, "bold"))
prompt_label.pack(side=tk.LEFT)

entry_command = tk.Entry(input_frame, font=("Consolas", 12))
entry_command.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry_command.focus_set()

entry_command.bind("<Return>", process_command)

print_to_console("Доступные команды: ls, cd, exit")

start_script_execution()

root.mainloop()