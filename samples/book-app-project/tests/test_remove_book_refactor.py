import sys
import os
from pathlib import Path
import json
import pytest

# Ensure the package path so 'books' can be imported from the samples directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import books
from books import BookCollection, Book


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test to avoid polluting the repository.

    Returns the Path object for tests that need to manipulate the file directly.
    """
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    return temp_file


def test_remove_existing_book_returns_true_and_removed():
    bc = BookCollection()
    bc.add_book("My Book", "Author", 2020)

    info = bc.remove_book("My Book", return_info=True)

    assert isinstance(info, dict)
    assert info["removed"] is True
    assert info["reason"] == "exact_match"
    assert info["matches"] == []
    assert bc.find_book_by_title("My Book") is None


def test_remove_case_insensitive_matching():
    bc = BookCollection()
    bc.add_book("Dune", "Frank Herbert", 1965)

    info = bc.remove_book("dUNE", return_info=True)

    assert info["removed"] is True
    assert info["reason"] == "exact_match"
    assert bc.find_book_by_title("Dune") is None


def test_remove_nonexistent_returns_not_found():
    bc = BookCollection()
    bc.add_book("Dune", "Frank Herbert", 1965)

    info = bc.remove_book("Unknown Title", return_info=True)

    assert info["removed"] is False
    assert info["reason"] == "not_found"
    assert info["matches"] == []


def test_remove_on_empty_collection_returns_not_found():
    bc = BookCollection()  # empty collection

    info = bc.remove_book("Anything", return_info=True)

    assert info["removed"] is False
    assert info["reason"] == "not_found"
    assert info["matches"] == []
