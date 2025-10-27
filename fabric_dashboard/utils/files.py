"""File I/O utilities for fabric_dashboard."""

import json
from pathlib import Path
from typing import Any, Optional


def ensure_dir(path: Path) -> None:
    """
    Ensure directory exists, create if it doesn't.

    Args:
        path: Directory path.
    """
    path.mkdir(parents=True, exist_ok=True)


def read_file(file_path: Path) -> str:
    """
    Read text file contents.

    Args:
        file_path: Path to file.

    Returns:
        File contents as string.

    Raises:
        FileNotFoundError: If file doesn't exist.
        IOError: If file can't be read.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Failed to read file {file_path}: {e}")


def write_file(file_path: Path, content: str) -> None:
    """
    Write text content to file.

    Args:
        file_path: Path to file.
        content: Content to write.

    Raises:
        IOError: If file can't be written.
    """
    try:
        # Ensure parent directory exists
        ensure_dir(file_path.parent)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise IOError(f"Failed to write file {file_path}: {e}")


def read_json(file_path: Path) -> Any:
    """
    Read and parse JSON file.

    Args:
        file_path: Path to JSON file.

    Returns:
        Parsed JSON data.

    Raises:
        FileNotFoundError: If file doesn't exist.
        json.JSONDecodeError: If JSON is invalid.
        IOError: If file can't be read.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {file_path}: {e.msg}", e.doc, e.pos)
    except Exception as e:
        raise IOError(f"Failed to read JSON file {file_path}: {e}")


def write_json(file_path: Path, data: Any, indent: int = 2) -> None:
    """
    Write data to JSON file.

    Args:
        file_path: Path to JSON file.
        data: Data to write (must be JSON-serializable).
        indent: Indentation spaces (default: 2).

    Raises:
        IOError: If file can't be written.
        TypeError: If data is not JSON-serializable.
    """
    try:
        # Ensure parent directory exists
        ensure_dir(file_path.parent)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
    except TypeError as e:
        raise TypeError(f"Data is not JSON-serializable: {e}")
    except Exception as e:
        raise IOError(f"Failed to write JSON file {file_path}: {e}")


def file_exists(file_path: Path) -> bool:
    """
    Check if file exists.

    Args:
        file_path: Path to file.

    Returns:
        True if file exists, False otherwise.
    """
    return file_path.exists() and file_path.is_file()


def dir_exists(dir_path: Path) -> bool:
    """
    Check if directory exists.

    Args:
        dir_path: Path to directory.

    Returns:
        True if directory exists, False otherwise.
    """
    return dir_path.exists() and dir_path.is_dir()


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes.

    Args:
        file_path: Path to file.

    Returns:
        File size in bytes.

    Raises:
        FileNotFoundError: If file doesn't exist.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return file_path.stat().st_size


def delete_file(file_path: Path) -> bool:
    """
    Delete a file.

    Args:
        file_path: Path to file.

    Returns:
        True if deleted, False if file didn't exist.

    Raises:
        IOError: If file can't be deleted.
    """
    if not file_path.exists():
        return False

    try:
        file_path.unlink()
        return True
    except Exception as e:
        raise IOError(f"Failed to delete file {file_path}: {e}")


def list_files(
    directory: Path, pattern: str = "*", recursive: bool = False
) -> list[Path]:
    """
    List files in directory matching pattern.

    Args:
        directory: Directory to search.
        pattern: Glob pattern (default: "*" for all files).
        recursive: Search recursively (default: False).

    Returns:
        List of file paths.

    Raises:
        FileNotFoundError: If directory doesn't exist.
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    if recursive:
        # Use rglob for recursive search
        return [p for p in directory.rglob(pattern) if p.is_file()]
    else:
        # Use glob for non-recursive search
        return [p for p in directory.glob(pattern) if p.is_file()]


def copy_file(source: Path, destination: Path, overwrite: bool = False) -> None:
    """
    Copy a file.

    Args:
        source: Source file path.
        destination: Destination file path.
        overwrite: Overwrite if destination exists (default: False).

    Raises:
        FileNotFoundError: If source doesn't exist.
        FileExistsError: If destination exists and overwrite=False.
        IOError: If file can't be copied.
    """
    import shutil

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    if destination.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {destination}")

    try:
        # Ensure destination directory exists
        ensure_dir(destination.parent)

        shutil.copy2(source, destination)
    except Exception as e:
        raise IOError(f"Failed to copy file from {source} to {destination}: {e}")


def get_unique_filename(directory: Path, base_name: str, extension: str) -> Path:
    """
    Generate unique filename by adding counter if file exists.

    Args:
        directory: Directory for the file.
        base_name: Base filename (without extension).
        extension: File extension (with or without dot).

    Returns:
        Unique file path.

    Examples:
        >>> get_unique_filename(Path("/tmp"), "dashboard", ".html")
        Path("/tmp/dashboard.html")  # or dashboard_1.html if exists
    """
    # Ensure extension starts with dot
    if not extension.startswith("."):
        extension = f".{extension}"

    file_path = directory / f"{base_name}{extension}"

    if not file_path.exists():
        return file_path

    # Add counter
    counter = 1
    while True:
        file_path = directory / f"{base_name}_{counter}{extension}"
        if not file_path.exists():
            return file_path
        counter += 1
