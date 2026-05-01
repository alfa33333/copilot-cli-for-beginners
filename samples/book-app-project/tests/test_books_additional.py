import sys
import os
from pathlib import Path
import pytest

# Ensure the samples/book-app-project directory is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import books
from books import BookCollection, Book


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test to avoid polluting the repo.

    The fixture writes an initial empty JSON array to the temp file and monkeypatches
    the module-level DATA_FILE used by the books module.
    """
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_persistence_across_instances():
    bc = BookCollection()
    bc.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    # Create a new collection instance that reloads from disk and verify persistence
    bc2 = BookCollection()
    found = bc2.find_book_by_title("the hobbit")
    assert found is not None
    assert found.author == "J.R.R. Tolkien"
    assert found.year == 1937
    assert found.read is False


def test_find_by_author_case_insensitive():
    bc = BookCollection()
    bc.add_book("A", "Jane Doe", 2001)
    bc.add_book("B", "jane doe", 2005)

    res = bc.find_by_author("JANE DOE")
    assert isinstance(res, list)
    assert len(res) == 2


def test_list_books_internal_mutation_affects_collection():
    bc = BookCollection()
    bc.add_book("X", "Y", 2000)

    books_list = bc.list_books()
    # Mutating the returned list should affect the internal collection (documented behavior)
    books_list.append(Book("Z", "Q", 2020))
    assert any(b.title == "Z" for b in bc.list_books())


def test_find_book_by_title_case_insensitive():
    bc = BookCollection()
    bc.add_book("Dune", "Frank Herbert", 1965)
    assert bc.find_book_by_title("dune") is not None


def test_load_corrupted_json_prints_warning(capsys):
    # Overwrite the temp data file with invalid JSON and instantiate a new collection
    Path(books.DATA_FILE).write_text("not valid json")
    _ = BookCollection()
    captured = capsys.readouterr()
    assert "corrupted" in captured.out
