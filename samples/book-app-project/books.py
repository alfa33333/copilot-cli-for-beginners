"""books.py — Book collection helpers used in course samples.

This module provides a lightweight Book dataclass and a BookCollection
class that manages an in-memory list of books persisted to a JSON file
(see DATA_FILE). The code is intentionally simple for teaching purposes.

Example:
    from samples.book_app_project.books import BookCollection

    bc = BookCollection()
    bc.add_book("Dune", "Frank Herbert", 1965)
"""
import json
import logging
from dataclasses import dataclass, asdict
from typing import List, Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DATA_FILE = "data.json"


@dataclass
class Book:
    """Data container for a book.

    Attributes:
        title (str): The book title.
        author (str): The author name.
        year (Optional[int]): Publication year (may be None if unknown).
        read (bool): Whether the book has been read. Defaults to False.

    Example:
        >>> b = Book('Dune', 'Frank Herbert', 1965)
        >>> b.read
        False
    """
    title: str
    author: str
    year: Optional[int] = None
    read: bool = False


class BookCollection:
    """Manage a collection of Book objects persisted to a JSON data file.

    The BookCollection class provides methods to load and save the collection,
    add/remove books, search by title, author, and year, and mark books as read.
    File I/O errors during save are propagated to callers; missing files are
    handled by initializing an empty collection. Corrupted JSON content is logged.

    Example:
        bc = BookCollection()
        bc.add_book("1984", "George Orwell", 1949)
    """

    def __init__(self):
        """Initialize a BookCollection.

        Loads existing books from DATA_FILE into the collection. If the data file
        does not exist or is corrupted, the collection will start empty (errors
        are handled by :meth:`load_books`).

        Returns:
            None

        Raises:
            None: :meth:`load_books` handles FileNotFoundError and JSONDecodeError internally.

        Example:
            >>> bc = BookCollection()
            >>> isinstance(bc, BookCollection)
            True
        """
        self.books: List[Book] = []
        self.load_books()

    @contextmanager
    def _open_data_file(self, mode: str = "r"):
        """Context manager for opening the data file.

        Centralizes file opening for read/write operations. Yields a file object
        opened with the given mode. Exceptions from opening the file are propagated
        to callers so they can handle them as needed.

        Parameters:
            mode (str): File open mode (e.g., 'r' or 'w').

        Yields:
            IO: An open file object.

        Raises:
            FileNotFoundError: If reading and the file does not exist.
            OSError: For other file-related errors.
        """
        f = open(DATA_FILE, mode)
        try:
            yield f
        finally:
            try:
                f.close()
            except Exception:
                pass

    def load_books(self):
        """Load books from the JSON file into the collection.

        Reads :data:`DATA_FILE` (JSON) and populates ``self.books`` with :class:`Book`
        instances. If the file does not exist, or if parsing fails, the collection
        is set to an empty list and no exception is propagated.

        Returns:
            None

        Raises:
            None: FileNotFoundError and json.JSONDecodeError are caught and handled.

        Example:
            >>> bc = BookCollection()
            >>> bc.load_books()  # reloads from disk
        """
        try:
            with self._open_data_file("r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Persist the current book collection to the JSON data file.

        Writes the in-memory list of :class:`Book` objects to ``DATA_FILE`` in JSON format.

        Returns:
            None

        Raises:
            OSError: If writing to the data file fails (e.g., permission denied,
                disk full). This exception is propagated to the caller.

        Example:
            >>> bc = BookCollection()
            >>> bc.add_book('1984', 'George Orwell', 1949)
            >>> bc.save_books()
        """
        with self._open_data_file("w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: Optional[int] = None) -> Book:
        """Add a new book to the collection and persist it to disk.

        Parameters:
            title (str): The title of the book.
            author (str): The author of the book.
            year (Optional[int]): The publication year, or None if unknown.

        Returns:
            Book: The :class:`Book` instance that was created and appended to the collection.

        Raises:
            OSError: If saving the updated collection to disk fails (propagated
                from :meth:`save_books`).

        Example:
            >>> bc = BookCollection()
            >>> book = bc.add_book('The Hobbit', 'J.R.R. Tolkien', 1937)
            >>> book.title
            'The Hobbit'
        """
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return the list of books in the collection.

        Note: This returns the internal list object. Mutating the returned list
        (e.g., ``.append()``, ``.remove()``) will modify the collection in memory.

        Returns:
            List[Book]: The list of :class:`Book` objects currently in the collection.

        Example:
            >>> bc = BookCollection()
            >>> books = bc.list_books()
            >>> isinstance(books, list)
            True
        """
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book in the collection by its title (case-insensitive).

        Parameters:
            title (str): The title to search for.

        Returns:
            Optional[Book]: The first matching :class:`Book` instance, or ``None`` if not found.

        Example:
            >>> bc = BookCollection()
            >>> bc.add_book('Dune', 'Frank Herbert', 1965)
            >>> bc.find_book_by_title('dune').author
            'Frank Herbert'
        """
        query = title.strip().casefold()
        for book in self.books:
            if book.title.strip().casefold() == query:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read by its title and persist the change.

        Parameters:
            title (str): The title of the book to mark as read (case-insensitive).

        Returns:
            bool: True if the book was found and marked as read; False otherwise.

        Raises:
            OSError: If saving the updated collection to disk fails (propagated
                from :meth:`save_books`).

        Example:
            >>> bc = BookCollection()
            >>> bc.add_book('Sapiens', 'Yuval Noah Harari', 2011)
            >>> bc.mark_as_read('sapiens')
            True
        """
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str, *, return_info: bool = False):
        """Remove a book from the collection by title and persist the change.

        Parameters:
            title (str): The title of the book to remove (case-insensitive).
            return_info (bool): When True, return a dict with details about the removal
                or why no removal occurred. When False (default), maintain previous
                behavior and return a boolean.

        Returns:
            bool or dict: If return_info is False, returns True if removed else False.
                If return_info is True, returns a dict with keys:
                - 'removed' (bool)
                - 'reason' (str): one of 'exact_match', 'partial_matches', 'word_matches', 'not_found'
                - 'matches' (list): list of dicts with candidate book info when not removed

        Raises:
            OSError: If saving the updated collection to disk fails (propagated
                from :meth:`save_books`).
        """
        query = title.strip().casefold()

        # Try exact match first
        for book in self.books:
            if book.title.strip().casefold() == query:
                self.books.remove(book)
                self.save_books()
                if return_info:
                    return {'removed': True, 'reason': 'exact_match', 'matches': []}
                return True

        # No exact match: look for partial matches (substring) and word overlap
        substring_matches = [b for b in self.books if query in b.title.strip().casefold()]
        if substring_matches:
            reason = 'partial_matches'
            matches = [{'title': b.title, 'author': b.author, 'year': b.year} for b in substring_matches]
            if return_info:
                return {'removed': False, 'reason': reason, 'matches': matches}
            return False

        # Word-overlap heuristic
        q_words = set(query.split())
        word_matches = []
        for b in self.books:
            b_words = set(b.title.strip().casefold().split())
            if q_words & b_words:
                word_matches.append(b)
        if word_matches:
            reason = 'word_matches'
            matches = [{'title': b.title, 'author': b.author, 'year': b.year} for b in word_matches]
            if return_info:
                return {'removed': False, 'reason': reason, 'matches': matches}
            return False

        # No matches found
        if return_info:
            return {'removed': False, 'reason': 'not_found', 'matches': []}
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Return all books by the given author (case-insensitive).

        Parameters:
            author (str): Author name to search for.

        Returns:
            List[Book]: A list of :class:`Book` instances written by the given author.
                Returns an empty list if no matches are found.

        Example:
            >>> bc = BookCollection()
            >>> bc.add_book('Book A', 'Jane Doe', 2000)
            >>> bc.add_book('Book B', 'Jane Doe', 2005)
            >>> len(bc.find_by_author('jane doe'))
            2
        """
        return [b for b in self.books if b.author.lower() == author.lower()]

    def find_by_year(self, start: Optional[int], end: Optional[int]) -> List[Book]:
        """Return books with known publication years between start and end (inclusive).

        Treats None and 0 as unknown years and excludes them from results.

        Parameters:
            start (Optional[int]): Inclusive lower bound year, or None for unbounded.
            end (Optional[int]): Inclusive upper bound year, or None for unbounded.

        Returns:
            List[Book]: Books whose publication year satisfies the inclusive range.

        Raises:
            ValueError: If both start and end are provided and start > end.

        Example:
            >>> bc = BookCollection()
            >>> bc.add_book('Old', 'A', 1950)
            >>> bc.add_book('New', 'B', 2000)
            >>> bc.find_by_year(1900, 1999)  # doctest: +ELLIPSIS
            [Book(...)]
        """
        if start is not None and end is not None and start > end:
            raise ValueError("start year must be <= end year")

        results: List[Book] = []
        for b in self.books:
            y = b.year
            if y is None or y == 0:
                continue
            if start is not None and y < start:
                continue
            if end is not None and y > end:
                continue
            results.append(b)
        return results

