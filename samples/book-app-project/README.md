# Book Collection App

*(This README is intentionally rough so you can improve it with GitHub Copilot CLI)*

A Python app for managing books you have or want to read.
It can add, remove, and list books. Also mark them as read.

---

## Current Features

* Reads books from a JSON file (our database)
* Publication year is optional in the UI — books without a year display as "Unknown"
* Input validation: required title; year input is validated and can be left blank (legacy behavior: blank/invalid year treated as 0)
* Search books by year (BookCollection.find_by_year): find books published between two inclusive years
* Some tests exist but probably not enough

---

## Files

* `book_app.py` - Main CLI entry point
* `books.py` - BookCollection class with data logic (now includes find_by_year)
* `utils.py` - Helper functions for UI and input (get_book_details now returns int year; 0 means unknown)
* `data.json` - Sample book data
* `tests/test_books.py` - Starter pytest tests
* `tests/test_find_by_year.py` - Tests for year-range search (new)

---

## Running the App

```bash
python book_app.py list
python book_app.py add
python book_app.py find
python book_app.py remove
python book_app.py search-year
python book_app.py help
```

Search by year (interactive)

Run `python book_app.py search-year` and follow the prompts to find books published between two years (inclusive).

Prompts
- Start year (optional): enter a year (e.g., `1990`) or press Enter for no lower bound.
- End year (optional): enter a year (e.g., `2005`) or press Enter for no upper bound.

Behavior
- Inclusive bounds: a book with year equal to the start or end is included.
- Blank input means unbounded (for example, blank start returns all books up to the end year).
- Books with unknown years (`None`) or the legacy value `0` are excluded from the results.

Example interactive session

```text
$ python book_app.py search-year
Start year (optional): 1990
End year (optional): 2005

Your Book Collection:
1. [ ] The Example Book by Jane Doe (1995)
2. [ ] Another Book by John Smith (2000)
```

Notes
- The command is interactive to match the existing `add` and `find` flows.
- For automation or scripting, consider adding non-interactive CLI flags in a future enhancement.

## Running Tests

```bash
python -m pytest tests/
```

---

## Notes

* Not production-ready (obviously)
* Docstrings updated: Book.year is now Optional[int]; BookCollection.find_by_year was added; utils.get_book_details now returns an int year (0 indicates unknown/legacy)
* The CLI UI accepts an optional year and shows "Unknown" when a year is not provided in display functions
* Consider cleaning up existing sample data (data.json) if it contains invalid placeholder years (e.g., 0)
* New tests added: tests/test_find_by_year.py
* Could add more commands later
