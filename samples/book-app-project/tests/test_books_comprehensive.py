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


def test_add_book_persists_and_returns_book(use_temp_data_file):
    bc = BookCollection()
    initial = len(bc.list_books())

    book = bc.add_book("Title1", "Author1", 2020)

    assert isinstance(book, Book)
    assert book.title == "Title1"
    assert book.author == "Author1"
    assert book.year == 2020
    assert book.read is False
    assert len(bc.list_books()) == initial + 1

    data = json.loads(Path(books.DATA_FILE).read_text())
    assert any(d.get("title") == "Title1" for d in data)


def test_remove_book_success_and_persists(use_temp_data_file):
    bc = BookCollection()
    bc.add_book("Rem1", "A", 1999)

    assert bc.remove_book("Rem1") is True
    assert bc.find_book_by_title("Rem1") is None

    data = json.loads(Path(books.DATA_FILE).read_text())
    assert not any(d.get("title") == "Rem1" for d in data)


def test_remove_book_nonexistent_returns_false(use_temp_data_file):
    bc = BookCollection()
    assert bc.remove_book("NoSuchBook") is False


def test_find_by_title_case_insensitive_and_duplicate(use_temp_data_file):
    bc = BookCollection()
    bc.add_book("Dup", "First", 2000)
    bc.add_book("Dup", "Second", 2010)

    found = bc.find_book_by_title("dup")
    assert found is not None
    # find_book_by_title returns the first matching book
    assert found.author == "First"


def test_find_by_author_case_insensitive(use_temp_data_file):
    bc = BookCollection()
    bc.add_book("A", "Jane Doe", 2000)
    bc.add_book("B", "jane doe", 2005)

    results = bc.find_by_author("JANE DOE")
    assert isinstance(results, list)
    assert len(results) == 2
    assert {b.title for b in results} == {"A", "B"}


def test_mark_as_read_sets_flag_and_persists(use_temp_data_file):
    bc = BookCollection()
    bc.add_book("ToRead", "Au", 2001)

    assert bc.mark_as_read("toread") is True
    b = bc.find_book_by_title("toread")
    assert b is not None and b.read is True

    data = json.loads(Path(books.DATA_FILE).read_text())
    assert any(d.get("title", "").lower() == "toread" and d.get("read") for d in data)


def test_mark_as_read_nonexistent_returns_false(use_temp_data_file):
    bc = BookCollection()
    assert bc.mark_as_read("nope") is False


def test_list_books_internal_mutation_affects_and_persists(use_temp_data_file):
    bc = BookCollection()
    bc.add_book("X", "Y", 2000)

    lst = bc.list_books()
    # Mutate the internal list (documented behavior)
    lst.append(Book("Z", "Q", 2020))
    assert any(b.title == "Z" for b in bc.list_books())

    # Persist and verify a new instance reloads the mutation
    bc.save_books()
    bc2 = BookCollection()
    assert any(b.title == "Z" for b in bc2.list_books())


def test_load_when_file_missing_starts_empty(use_temp_data_file):
    # Remove the temp file to simulate a missing data file
    Path(books.DATA_FILE).unlink()
    bc = BookCollection()
    assert bc.list_books() == []


def test_load_corrupted_json_prints_warning(use_temp_data_file, capsys):
    Path(books.DATA_FILE).write_text("not valid json")
    _ = BookCollection()
    captured = capsys.readouterr()
    assert "corrupted" in captured.out
