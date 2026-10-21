import tkinter as tk
import os
import socket
import getpass
import argparse
import csv
import base64

parser = argparse.ArgumentParser()
parser.add_argument("--vfs", type=str, default="vfs_default.csv")
parser.add_argument("--script", type=str)
args = parser.parse_args()

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

class VirtualFileSystem:
    def __init__(self, startup_path):
        self.fs = {}
        self.cwd = "/"
        self.default_vfs_path = "vfs_default.csv"
        self.init_fs(startup_path)

    def init_fs(self, path_to_load):
        self.fs = {"/": {"type": "dir"}}
        self.cwd = "/"
        try:
            with open(path_to_load, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    path = row['path'].strip()
                    ftype = row['type'].strip()
                    content = row.get('content', '').strip()
                    
                    if not path or path == "/": continue
                    
                    self.fs[path] = {"type": ftype, "content": content}
            return True
        except FileNotFoundError:
            return False
        
    def _resolve_path(self, path):
        if not path:
            return self.cwd
        
        if path.startswith("/"):
            new_path = path
        else:
            new_path = os.path.join(self.cwd, path)

        parts = new_path.split("/")
        normalized = []
        for part in parts:
            if part == "" or part == ".":
                continue
            elif part == "..":
                if normalized: normalized.pop()
            else:
                normalized.append(part)
        return "/" + "/".join(normalized)

    def ls(self, path_arg=None):
        target_path = self._resolve_path(path_arg) if path_arg else self.cwd
        if target_path not in self.fs:
            return f"ls: cannot access '{target_path}': No such file or directory"
        if self.fs[target_path]["type"] != "dir":
            return target_path
    
        children = []
        for p in self.fs:
            if p == target_path: continue
            parent = os.path.dirname(p) if p != "/" else "/"
            if parent == target_path:
                name = os.path.basename(p)
                if self.fs[p]["type"] == "dir":
                    name += "/"
                children.append(name)
        
        return "  ".join(sorted(children)) if children else ""

    def cd(self, path_arg):
        if not path_arg:
            self.cwd = "/"
            return True, ""
        
        target_path = self._resolve_path(path_arg)
        if target_path not in self.fs:
            return False, f"cd: {path_arg}: No such file or directory"
        if self.fs[target_path]["type"] != "dir":
            return False, f"cd: {path_arg}: Not a directory"
            
        self.cwd = target_path
        return True, ""

    def cat(self, path_arg):
        if not path_arg:
            return False, "cat: missing file operand"
        target_path = self._resolve_path(path_arg)
        if target_path not in self.fs:
            return False, f"cat: {path_arg}: No such file or directory"
        if self.fs[target_path]["type"] == "dir":
            return False, f"cat: {path_arg}: Is a directory"

        try:
            content_b64 = self.fs[target_path]["content"]
            decoded_bytes = base64.b64decode(content_b64)
            return True, decoded_bytes.decode('utf-8', errors='replace')
        except Exception as e:
            return False, f"cat: error reading file - {e}"

vfs = VirtualFileSystem(args.vfs)





def print_to_console(text):
    console_text.config(state=tk.NORMAL)
    console_text.insert(tk.END, text + "\n")
    console_text.see(tk.END)
    console_text.config(state=tk.DISABLED)

def update_header():
    prompt_label.config(text=f"[{username}@{hostname} {vfs.cwd}]$ ")

def execute_command(full_command):
    if not full_command:
        return True

    parts = full_command.split()
    command = parts[0]
    cmd_args = parts[1:] if len(parts) > 1 else []

    if command == "ls":
        result = vfs.ls(cmd_args[0] if cmd_args else None)
        if result: print_to_console(result)
        return True
        
    elif command == "cd":
        success, msg = vfs.cd(cmd_args[0] if cmd_args else "")
        if not success:
            print_to_console(msg)
            return False
        update_header()
        return True
        
    elif command == "cat":
        success, msg = vfs.cat(cmd_args[0] if cmd_args else None)
        print_to_console(msg)
        return success

    elif command == "vfs-init":
        if vfs.init_fs(vfs.default_vfs_path):
            print_to_console("VFS успешно инициализирована заново.")
            update_header()
            return True
        else:
            print_to_console(f"Ошибка: не удалось найти базовый файл VFS ({vfs.default_vfs_path})")
            return False

    elif command == "exit":
        print_to_console("Завершение работы эмулятора")
        root.after(500, root.destroy)
        return True
        
    else:
        print_to_console(f"Эмулятор: команда '{command}' не найдена")
        return False

def process_command(event=None):
    full_command = entry_command.get().strip()
    entry_command.delete(0, tk.END)
    if not full_command: return

    print_to_console(f"[{username}@{hostname} {vfs.cwd}]$ {full_command}")
    execute_command(full_command)

script_lines = []
current_line_index = 0

def run_next_script_line():
    global current_line_index
    if current_line_index >= len(script_lines):
        print_to_console("Скрипт завершил работу")
        return

    line = script_lines[current_line_index].strip()
    current_line_index += 1

    if not line or line.startswith("#"):
        root.after(50, run_next_script_line)
        return

    print_to_console(f"[{username}@{hostname} {vfs.cwd}]$ {line}")
    success = execute_command(line)
    
    if success:
        root.after(400, run_next_script_line)
    else:
        print_to_console("Выполнение скрипта остановлено из-за ошибки")

def start_script_execution():
    global script_lines
    if args.script:
        try:
            with open(args.script, 'r', encoding='utf-8') as f:
                script_lines = f.readlines()
            print_to_console(f"[Запуск скрипта: {args.script}]")
            root.after(500, run_next_script_line)
        except FileNotFoundError:
            print_to_console(f"Ошибка: '{args.script}' не найден")

root = tk.Tk()
root.title(window_title)
root.geometry("800x600")

console_text = tk.Text(root, bg="black", fg="#1900ff", font=("Consolas", 12), wrap="word")
console_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
console_text.config(state=tk.DISABLED)

input_frame = tk.Frame(root)
input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

prompt_label = tk.Label(input_frame, text=f"[{username}@{hostname} {vfs.cwd}]$ ", font=("Consolas", 12, "bold"))
prompt_label.pack(side=tk.LEFT)

entry_command = tk.Entry(input_frame, font=("Consolas", 12))
entry_command.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry_command.focus_set()

entry_command.bind("<Return>", process_command)

print_to_console("Доступные команды: ls, cd, cat, vfs-init, exit")
print_to_console("Текущая директория: /")

start_script_execution()
root.mainloop()