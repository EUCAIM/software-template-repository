from pathlib import Path
from typing import Any, List
import shutil
import json


def load_json(path: Path) -> Any:
    """
    Loads a JSON file from the specified path.

    Args:
        path: A Path representing the file path.

    Returns:
        The data loaded from the JSON file.
    """
    with open(path, 'r') as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    """
    Saves data to a JSON file at the specified path.

    Args:
        path: A Path representing the file path.
        data: The data to be serialized and saved.
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def load_jsonl(path: Path) -> List[Any]:
    """
    Loads a JSONL file (JSON lines) from the specified path.

    Args:
        path: A Path representing the file path.

    Returns:
        A list of data loaded from the JSONL file.
    """
    with open(path, 'r') as f:
        return [json.loads(line) for line in f]


def save_jsonl(path: Path, data: List[Any]) -> None:
    """
    Saves data to a JSONL file at the specified path.

    Args:
        path: A Path representing the file path.
        data: A list of data to be serialized and saved.
    """
    with open(path, 'w') as f:
        for line in data:
            json.dump(line, f)
            f.write('\n')


def maybe_make_dir(path: str) -> Path:
    """
    Creates a directory at the specified path if it does not exist.

    Args:
        path: A string representing the directory path.

    Returns:
        A Path object for the created or existing directory.
    """
    dir = Path(path)
    if not dir.exists():
        dir.mkdir(parents=True)
    return dir


def maybe_remove_dir(path: str) -> Path:
    path_obj = Path(path)
    if path_obj.exists() and path_obj.is_dir():
        try:
            shutil.rmtree(path_obj)
            print(f"Directory {path} removed successfully.")
        except Exception as e:
            print(f"Error removing directory {path}: {e}")
    return path_obj
