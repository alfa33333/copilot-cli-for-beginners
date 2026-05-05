import sys
import os
<<<<<<< HEAD
import builtins
import pytest

# Ensure the samples/book-app-project directory is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils


def test_get_book_details_valid_input(monkeypatch):
    inputs = iter(["Good Title", "Author Name", "2001"])
    monkeypatch.setattr(builtins, "input", lambda prompt='': next(inputs))

    title, author, year = utils.get_book_details()

    assert title == "Good Title"
    assert author == "Author Name"
    assert year == 2001


def test_get_book_details_empty_title_reprompt(monkeypatch, capsys):
    # First input is empty; function should re-prompt and print a message
    inputs = iter(["", "Final Title", "Author", "1999"])
    monkeypatch.setattr(builtins, "input", lambda prompt='': next(inputs))

    title, author, year = utils.get_book_details()
    captured = capsys.readouterr()

    assert "Title cannot be empty" in captured.out
    assert title == "Final Title"
    assert author == "Author"
    assert year == 1999


def test_get_book_details_invalid_year_defaults_zero(monkeypatch, capsys):
    inputs = iter(["Some Book", "An Author", "notanumber"])
    monkeypatch.setattr(builtins, "input", lambda prompt='': next(inputs))

    title, author, year = utils.get_book_details()
    captured = capsys.readouterr()

    assert "Invalid year" in captured.out
    assert year == 0


def test_get_book_details_year_blank_defaults_zero(monkeypatch, capsys):
    inputs = iter(["Blank Year Book", "Author", ""])
    monkeypatch.setattr(builtins, "input", lambda prompt='': next(inputs))

    title, author, year = utils.get_book_details()
    captured = capsys.readouterr()

    assert "Invalid year" in captured.out
    assert year == 0


def test_get_book_details_very_long_title(monkeypatch):
    long_title = "A" * 5000
    inputs = iter([long_title, "Author Long", "2015"])
    monkeypatch.setattr(builtins, "input", lambda prompt='': next(inputs))

    title, author, year = utils.get_book_details()

    assert title == long_title
    assert len(title) == 5000
    assert year == 2015


def test_get_book_details_special_characters_author(monkeypatch):
    special_author = "José Ángel 😊 - O'Neill"
    inputs = iter(["Some Title", special_author, "1995"])
    monkeypatch.setattr(builtins, "input", lambda prompt='': next(inputs))

    title, author, year = utils.get_book_details()

    assert author == special_author
    assert year == 1995


def test_get_book_details_author_empty_allowed(monkeypatch):
    inputs = iter(["Title Only", "", "2007"])
    monkeypatch.setattr(builtins, "input", lambda prompt='': next(inputs))

    title, author, year = utils.get_book_details()

    assert author == ""
    assert title == "Title Only"
    assert year == 2007


def test_get_book_details_title_whitespace_only_reprompt(monkeypatch, capsys):
    # Whitespace-only inputs are stripped and treated as empty
    inputs = iter(["   ", "\t", "Real Title", "Auth", "2020"])
    monkeypatch.setattr(builtins, "input", lambda prompt='': next(inputs))

    title, author, year = utils.get_book_details()
    captured = capsys.readouterr()

    assert "Title cannot be empty" in captured.out
    assert title == "Real Title"
    assert author == "Auth"
    assert year == 2020


def test_get_user_choice_valid(monkeypatch):
    for choice in ["1", "2", "3", "4", "5"]:
        monkeypatch.setattr(builtins, "input", lambda prompt='': choice)
        result = utils.get_user_choice()
        assert result == choice


def test_get_user_choice_invalid_then_valid(monkeypatch, capsys):
    inputs = iter(["0", "6", "abc", "3"])
    monkeypatch.setattr(builtins, "input", lambda prompt='': next(inputs))
    result = utils.get_user_choice()
    captured = capsys.readouterr()
    assert result == "3"
    assert "Invalid choice" in captured.out or "Invalid input" in captured.out or "Choice out of range" in captured.out
=======
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import patch
from utils import get_book_details, get_user_choice


def test_get_book_details_valid_input():
    with patch("builtins.input", side_effect=["The Hobbit", "Tolkien", "1937"]):
        title, author, year = get_book_details()
    assert title == "The Hobbit"
    assert author == "Tolkien"
    assert year == 1937


def test_get_book_details_empty_title_reprompt():
    with patch("builtins.input", side_effect=["", "Valid Title", "Author", "2000"]):
        title, author, year = get_book_details()
    assert title == "Valid Title"


def test_get_book_details_invalid_year_defaults_zero():
    with patch("builtins.input", side_effect=["Title", "Author", "not-a-year"]):
        title, author, year = get_book_details()
    assert year == 0


def test_get_book_details_year_blank_defaults_zero():
    with patch("builtins.input", side_effect=["Title", "Author", ""]):
        title, author, year = get_book_details()
    assert year == 0


def test_get_book_details_very_long_title():
    long_title = "A" * 1000
    with patch("builtins.input", side_effect=[long_title, "Author", "2000"]):
        title, author, year = get_book_details()
    assert title == long_title


def test_get_book_details_special_characters_author():
    with patch("builtins.input", side_effect=["My Book", "O'Brien & Müller", "2020"]):
        title, author, year = get_book_details()
    assert author == "O'Brien & Müller"


def test_get_book_details_author_empty_allowed():
    with patch("builtins.input", side_effect=["Title", "", "2020"]):
        title, author, year = get_book_details()
    assert author == ""


def test_get_book_details_title_whitespace_only_reprompt():
    with patch("builtins.input", side_effect=["   ", "Real Title", "Author", "2020"]):
        title, author, year = get_book_details()
    assert title == "Real Title"


def test_get_user_choice_valid():
    for choice in ["1", "2", "3", "4", "5"]:
        with patch("builtins.input", return_value=choice):
            result = get_user_choice()
        assert result == choice


def test_get_user_choice_invalid_then_valid(capsys):
    with patch("builtins.input", side_effect=["0", "6", "abc", "3"]):
        result = get_user_choice()
    assert result == "3"
    captured = capsys.readouterr()
    assert "Invalid choice" in captured.out
>>>>>>> origin/main
