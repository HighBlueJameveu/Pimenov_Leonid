import tkinter as tk
import os
import socket
import getpass

try:
    username = getpass.getuser()
except Exception:
    username = "unknown_user"

try:
    hostname = socket.gethostname()
except Exception:
    hostname = "unknown_host"

window_title = f"Эмулятор - [{username}@{hostname}]"


# --- 2. Основные функции приложения ---

def print_to_console(text):
    console_text.config(state=tk.NORMAL)  
    console_text.insert(tk.END, text + "\n") 
    console_text.see(tk.END)       
    console_text.config(state=tk.DISABLED)


def process_command(event=None):
    """Функция, которая вызывается при нажатии Enter в поле ввода."""
    full_command = entry_command.get().strip()

    entry_command.delete(0, tk.END)

    if not full_command:
        return

    print_to_console(f"[{username}@{hostname}]$ {full_command}")
    
    parts = full_command.split()
    command = parts[0]
    args = parts[1:]

    if command == "ls":
        # Команда-заглушка
        print_to_console(f"Эмулятор: Команда 'ls' вызвана с аргументами: {args}")
        
    elif command == "cd":
        # Команда-заглушка
        print_to_console(f"Эмулятор: Команда 'cd' вызвана с аргументами: {args}")
        
    elif command == "exit":
        # Команда выхода
        print_to_console("Завершение работы эмулятора")
        root.after(500, root.destroy) 
        
    else:
        print_to_console(f"Эмулятор: команда '{command}' не найдена")

root = tk.Tk()
root.title(window_title)
root.geometry("800x600")

console_text = tk.Text(root, bg="black", fg="white", font=("Consolas", 12), wrap="word")
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

root.mainloop()