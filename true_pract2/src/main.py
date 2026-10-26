import sys
import argparse
import urllib.parse
from pathlib import Path
from apk_parser import read_local_index, download_index, extract_index_text, parse_dependencies
from graph_builder import load_test_graph_from_txt, build_transitive_graph, draw_and_save_graph

try:
    import tomllib
except ImportError:
    print("Ошибка: Для работы требуется Python 3.11+")
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
        if not Path(source).exists():
            raise FileNotFoundError(f"Файл репозитория не найден: {source}")
    else:
        parsed = urllib.parse.urlparse(source)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"Неверный URL '{source}'.")


def validate_test_mode(mode: bool) -> None:
    if not isinstance(mode, bool):
        raise ValueError("Параметр 'test_mode' должен быть логическим значением")


def validate_output_file(filename: str) -> None:
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("Параметр 'output_file' должен быть непустым")
    allowed_extensions = {".png", ".svg", ".pdf", ".jpg"}
    if Path(filename).suffix.lower() not in allowed_extensions:
        raise ValueError(f"Файл '{filename}' должен иметь расширение: {allowed_extensions}")


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


def get_dependencies_callback(config: dict):
    if config["repo_url"].endswith(".txt"):
        test_graph = load_test_graph_from_txt(config["repo_url"])
        return lambda pkg: test_graph.get(pkg, [])
    else:
        if config["test_mode"]:
            raw_data = read_local_index(config["repo_url"])
        else:
            raw_data = download_index(config["repo_url"])
        index_text = extract_index_text(raw_data)
        
        return lambda pkg: parse_dependencies(index_text, pkg)


def main() -> None:
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей")
    parser.add_argument("--config", default="config.toml", help="Путь к TOML")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        validate_config(config)
        print_config(config)
        
        print("\nПостроение графа")
        deps_func = get_dependencies_callback(config)
        
        print("BFS")
        graph = build_transitive_graph(config["package_name"], deps_func)

        print(f"Узлов в графе: {graph.number_of_nodes()}, связей: {graph.number_of_edges()}")
        draw_and_save_graph(graph, config["output_file"])
        
    except Exception as e:
        print(f"ОШИБКА {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()