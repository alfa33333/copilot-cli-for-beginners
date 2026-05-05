import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def titles_of(items):
    return {b.title for b in items}


def test_find_by_year_various_ranges():
    collection = BookCollection()
    collection.add_book("Old Book", "Author A", 1950)
    collection.add_book("Mid Book", "Author B", 1995)
    collection.add_book("New Book", "Author C", 2010)
    collection.add_book("Unknown", "Author D", None)
    collection.add_book("Legacy Zero", "Author E", 0)

    assert titles_of(collection.find_by_year(1950, 2010)) == {"Old Book", "Mid Book", "New Book"}
    assert titles_of(collection.find_by_year(None, 1999)) == {"Old Book", "Mid Book"}
    assert titles_of(collection.find_by_year(1996, None)) == {"New Book"}
    assert titles_of(collection.find_by_year(None, None)) == {"Old Book", "Mid Book", "New Book"}

    with pytest.raises(ValueError):
        collection.find_by_year(2000, 1990)
