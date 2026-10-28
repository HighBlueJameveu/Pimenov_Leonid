import io
import urllib.request
import tarfile
from pathlib import Path

INDEX_FILENAME = "APKINDEX"
TAG_PACKAGE = "P:"
TAG_DEPENDS = "D:"
BLOCK_SEPARATOR = "\n\n"


def download_index(url: str) -> bytes:
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except Exception as e:
        raise RuntimeError(f"Ошибка при скачивании индекса: {e}")


def read_local_index(filepath: str) -> bytes:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Локальный файл не найден: {filepath}")
    with open(path, "rb") as f:
        return f.read()


def extract_index_text(archive_bytes: bytes) -> str:
    try:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as tar:
            member = tar.getmember(INDEX_FILENAME)
            file_obj = tar.extractfile(member)
            if file_obj is None:
                raise ValueError("Не удалось извлечь APKINDEX из архива")
            return file_obj.read().decode("utf-8")
    except tarfile.TarError as e:
        raise ValueError(f"Ошибка распаковки архива: {e}")


def parse_dependencies(index_text: str, package_name: str) -> list[str]:
    blocks = index_text.split(BLOCK_SEPARATOR)
    target_tag = f"{TAG_PACKAGE}{package_name}"

    for block in blocks:
        lines = block.strip().split("\n")

        if any(line == target_tag for line in lines):
            for line in lines:
                if line.startswith(TAG_DEPENDS):
                    deps_str = line[len(TAG_DEPENDS):].strip()
                    return deps_str.split() if deps_str else []
            return [] 

    raise ValueError(f"Пакет '{package_name}' не найден в индексе.")


def get_package_dependencies(config: dict) -> list[str]:
    if config["test_mode"]:
        raw_data = read_local_index(config["repo_url"])
    else:
        raw_data = download_index(config["repo_url"])

    index_text = extract_index_text(raw_data)
    return parse_dependencies(index_text, config["package_name"])