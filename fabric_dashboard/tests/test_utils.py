"""Unit tests for utility modules."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from fabric_dashboard.models.schemas import Config
from fabric_dashboard.utils import cache, config, files


# ============================================================================
# CONFIG TESTS
# ============================================================================


def test_ensure_config_dir(tmp_path, monkeypatch):
    """Test config directory creation."""
    # Mock CONFIG_DIR to use temp directory
    test_config_dir = tmp_path / ".fabric-dashboard"
    monkeypatch.setattr(config, "CONFIG_DIR", test_config_dir)
    monkeypatch.setattr(config, "CONFIG_FILE", test_config_dir / "config.yaml")
    monkeypatch.setattr(config, "DASHBOARDS_DIR", test_config_dir / "dashboards")

    config.ensure_config_dir()

    assert test_config_dir.exists()
    assert (test_config_dir / "dashboards").exists()


def test_save_and_load_config(tmp_path, monkeypatch):
    """Test saving and loading configuration."""
    # Mock CONFIG_DIR
    test_config_dir = tmp_path / ".fabric-dashboard"
    test_config_file = test_config_dir / "config.yaml"
    monkeypatch.setattr(config, "CONFIG_DIR", test_config_dir)
    monkeypatch.setattr(config, "CONFIG_FILE", test_config_file)
    monkeypatch.setattr(config, "DASHBOARDS_DIR", test_config_dir / "dashboards")

    # Create config
    test_config = Config(
        anthropic_api_key="sk-test-123",
        perplexity_api_key="pplx-test-456",
        days_back=30,
    )

    # Save config
    config.save_config(test_config)

    assert test_config_file.exists()

    # Load config
    loaded_config = config.load_config()

    assert loaded_config is not None
    assert loaded_config.anthropic_api_key == "sk-test-123"
    assert loaded_config.perplexity_api_key == "pplx-test-456"
    assert loaded_config.days_back == 30


def test_load_config_nonexistent(tmp_path, monkeypatch):
    """Test loading config when file doesn't exist."""
    test_config_file = tmp_path / "nonexistent.yaml"
    monkeypatch.setattr(config, "CONFIG_FILE", test_config_file)

    loaded_config = config.load_config()
    assert loaded_config is None


def test_get_config_from_env(monkeypatch):
    """Test loading config from environment variables."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-env-test")
    monkeypatch.setenv("PERPLEXITY_API_KEY", "pplx-env-test")
    monkeypatch.setenv("DAYS_BACK", "60")
    monkeypatch.setenv("DEBUG", "true")

    env_config = config.get_config_from_env()

    assert env_config is not None
    assert env_config.anthropic_api_key == "sk-env-test"
    assert env_config.perplexity_api_key == "pplx-env-test"
    assert env_config.days_back == 60
    assert env_config.debug is True


def test_get_config_from_env_missing_keys(monkeypatch):
    """Test that missing environment variables return None."""
    # Clear any existing env vars
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("PERPLEXITY_API_KEY", raising=False)

    env_config = config.get_config_from_env()
    assert env_config is None


# ============================================================================
# CACHE TESTS
# ============================================================================


def test_search_cache_basic(tmp_path):
    """Test basic cache operations."""
    cache_dir = tmp_path / "test_cache"
    search_cache = cache.SearchCache(ttl=60)
    search_cache.cache_dir = cache_dir

    # Test set and get
    query = "test query"
    result = {"data": "test result"}

    search_cache.set(query, result)
    cached_result = search_cache.get(query)

    assert cached_result == result

    # Test has
    assert search_cache.has(query) is True
    assert search_cache.has("nonexistent query") is False

    # Clean up
    search_cache.close()


def test_search_cache_delete(tmp_path):
    """Test cache deletion."""
    cache_dir = tmp_path / "test_cache"
    search_cache = cache.SearchCache(ttl=60)
    search_cache.cache_dir = cache_dir

    query = "test query"
    result = {"data": "test"}

    search_cache.set(query, result)
    assert search_cache.has(query) is True

    # Delete
    deleted = search_cache.delete(query)
    assert deleted is True
    assert search_cache.has(query) is False

    # Try deleting non-existent
    deleted_again = search_cache.delete(query)
    assert deleted_again is False

    search_cache.close()


def test_search_cache_clear(tmp_path):
    """Test clearing entire cache."""
    cache_dir = tmp_path / "test_cache"
    search_cache = cache.SearchCache(ttl=60)
    search_cache.cache_dir = cache_dir

    # Add multiple items
    for i in range(5):
        search_cache.set(f"query_{i}", {"data": i})

    stats = search_cache.stats()
    assert stats["size"] == 5

    # Clear
    search_cache.clear()

    stats_after = search_cache.stats()
    assert stats_after["size"] == 0

    search_cache.close()


def test_search_cache_context_manager(tmp_path):
    """Test cache as context manager."""
    cache_dir = tmp_path / "test_cache"

    with cache.SearchCache(ttl=60) as search_cache:
        search_cache.cache_dir = cache_dir
        search_cache.set("test", "value")
        assert search_cache.get("test") == "value"

    # Cache should be closed after context


# ============================================================================
# FILES TESTS
# ============================================================================


def test_ensure_dir(tmp_path):
    """Test directory creation."""
    test_dir = tmp_path / "test" / "nested" / "dir"

    files.ensure_dir(test_dir)

    assert test_dir.exists()
    assert test_dir.is_dir()


def test_read_write_file(tmp_path):
    """Test reading and writing text files."""
    test_file = tmp_path / "test.txt"
    content = "Hello, world!\nLine 2"

    # Write
    files.write_file(test_file, content)
    assert test_file.exists()

    # Read
    read_content = files.read_file(test_file)
    assert read_content == content


def test_read_file_not_found(tmp_path):
    """Test reading non-existent file raises error."""
    test_file = tmp_path / "nonexistent.txt"

    with pytest.raises(FileNotFoundError):
        files.read_file(test_file)


def test_read_write_json(tmp_path):
    """Test reading and writing JSON files."""
    test_file = tmp_path / "test.json"
    data = {"key": "value", "number": 42, "list": [1, 2, 3]}

    # Write
    files.write_json(test_file, data)
    assert test_file.exists()

    # Read
    read_data = files.read_json(test_file)
    assert read_data == data


def test_read_json_invalid(tmp_path):
    """Test reading invalid JSON raises error."""
    test_file = tmp_path / "invalid.json"

    # Write invalid JSON
    with open(test_file, "w") as f:
        f.write("{ invalid json }")

    with pytest.raises(json.JSONDecodeError):
        files.read_json(test_file)


def test_file_exists(tmp_path):
    """Test file existence check."""
    existing_file = tmp_path / "exists.txt"
    existing_file.touch()

    assert files.file_exists(existing_file) is True
    assert files.file_exists(tmp_path / "nonexistent.txt") is False


def test_dir_exists(tmp_path):
    """Test directory existence check."""
    existing_dir = tmp_path / "exists"
    existing_dir.mkdir()

    assert files.dir_exists(existing_dir) is True
    assert files.dir_exists(tmp_path / "nonexistent") is False


def test_get_file_size(tmp_path):
    """Test getting file size."""
    test_file = tmp_path / "test.txt"
    content = "Hello, world!"

    files.write_file(test_file, content)

    size = files.get_file_size(test_file)
    assert size == len(content.encode("utf-8"))


def test_delete_file(tmp_path):
    """Test deleting files."""
    test_file = tmp_path / "test.txt"
    test_file.touch()

    assert test_file.exists()

    # Delete
    deleted = files.delete_file(test_file)
    assert deleted is True
    assert not test_file.exists()

    # Try deleting again
    deleted_again = files.delete_file(test_file)
    assert deleted_again is False


def test_list_files(tmp_path):
    """Test listing files in directory."""
    # Create some files
    (tmp_path / "file1.txt").touch()
    (tmp_path / "file2.txt").touch()
    (tmp_path / "file3.json").touch()

    # List all files
    all_files = files.list_files(tmp_path)
    assert len(all_files) == 3

    # List with pattern
    txt_files = files.list_files(tmp_path, pattern="*.txt")
    assert len(txt_files) == 2


def test_list_files_recursive(tmp_path):
    """Test recursive file listing."""
    # Create nested structure
    (tmp_path / "file1.txt").touch()
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "file2.txt").touch()

    # Non-recursive
    files_non_recursive = files.list_files(tmp_path, pattern="*.txt", recursive=False)
    assert len(files_non_recursive) == 1

    # Recursive
    files_recursive = files.list_files(tmp_path, pattern="*.txt", recursive=True)
    assert len(files_recursive) == 2


def test_copy_file(tmp_path):
    """Test copying files."""
    source = tmp_path / "source.txt"
    destination = tmp_path / "dest.txt"

    files.write_file(source, "test content")

    files.copy_file(source, destination)

    assert destination.exists()
    assert files.read_file(destination) == "test content"


def test_copy_file_overwrite(tmp_path):
    """Test copying file with overwrite."""
    source = tmp_path / "source.txt"
    destination = tmp_path / "dest.txt"

    files.write_file(source, "new content")
    files.write_file(destination, "old content")

    # Should raise without overwrite
    with pytest.raises(FileExistsError):
        files.copy_file(source, destination, overwrite=False)

    # Should work with overwrite
    files.copy_file(source, destination, overwrite=True)
    assert files.read_file(destination) == "new content"


def test_get_unique_filename(tmp_path):
    """Test generating unique filenames."""
    # First file should be base name
    file1 = files.get_unique_filename(tmp_path, "dashboard", ".html")
    assert file1 == tmp_path / "dashboard.html"

    # Create the file
    file1.touch()

    # Next file should have counter
    file2 = files.get_unique_filename(tmp_path, "dashboard", ".html")
    assert file2 == tmp_path / "dashboard_1.html"

    # Create that too
    file2.touch()

    # Next should increment
    file3 = files.get_unique_filename(tmp_path, "dashboard", ".html")
    assert file3 == tmp_path / "dashboard_2.html"
