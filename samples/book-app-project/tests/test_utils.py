import sys
import os
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
