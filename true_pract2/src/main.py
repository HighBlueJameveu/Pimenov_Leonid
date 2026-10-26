import sys
import argparse
import urllib.parse
from pathlib import Path
from apk_parser import get_package_dependencies

try:
    import tomllib
except ImportError:
    print("Ошибка: Для работы требуется Python 3.11+ (встроенный модуль tomllib).")
    sys.exit(1)


def load_config(filepath: str) -> dict:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Файл конфигурации не найден: {filepath}")
    
    if not path.is_file():
        raise IsADirectoryError(f"Указанный путь не является файлом: {filepath}")

    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"Ошибка синтаксиса в TOML-файле: {e}")


def validate_package_name(name: str) -> None:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Параметр 'package_name' должен быть непустым")


def validate_repo_source(source: str, is_test_mode: bool) -> None:
    if not isinstance(source, str) or not source.strip():
        raise ValueError("Параметр 'repo_url' должен быть непустым")
    
    if is_test_mode:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Файл репозитория не найден: {source}")
    else:
        parsed = urllib.parse.urlparse(source)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"Неверный URL '{source}'. Схема должна быть http или https.")


def validate_test_mode(mode: bool) -> None:
    if not isinstance(mode, bool):
        raise ValueError("Параметр 'test_mode' должен быть логическим значением")


def validate_output_file(filename: str) -> None:
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("Параметр 'output_file' должен быть непустым")
    
    allowed_extensions = {".png", ".svg", ".pdf", ".jpg"}
    ext = Path(filename).suffix.lower()
    if ext not in allowed_extensions:
        raise ValueError(f"Файл '{filename}' должен иметь одно из расширений: {allowed_extensions}")


def validate_config(config: dict) -> None:
    required_keys = ["package_name", "repo_url", "test_mode", "output_file"]
    
    for key in required_keys:
        if key not in config:
            raise KeyError(f"Отсутствует обязательный параметр: '{key}'")

    validate_package_name(config["package_name"])
    validate_test_mode(config["test_mode"])
    validate_repo_source(config["repo_url"], config["test_mode"])
    validate_output_file(config["output_file"])


def print_config(config: dict) -> None:
    print("Текущие настройки")
    print(f"package_name : {config['package_name']}")
    print(f"repo_url     : {config['repo_url']}")
    print(f"test_mode    : {str(config['test_mode']).lower()}")
    print(f"output_file  : {config['output_file']}")



def main() -> None:
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей пакетов")
    parser.add_argument(
        "--config", 
        default="config.toml", 
        help="Путь к TOML-файлу конфигурации"
    )
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        validate_config(config)
        print_config(config)

        print("\nПоиск зависимостей")
        deps = get_package_dependencies(config)
        
        if not deps:
            print(f"У пакета '{config['package_name']}' нет прямых зависимостей.")
        else:
            print(f"Прямые зависимости пакета '{config['package_name']}':")
            for dep in deps:
                print(f" - {dep}")

    except Exception as e:
        print(f"ОШИБКА {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()