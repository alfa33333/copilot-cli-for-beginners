import logging
logger = logging.getLogger(__name__)

def print_menu():
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()
<<<<<<< HEAD
        if not choice:
            print("Please enter a choice (1-5).")
            continue
        if not choice.isdigit():
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue
        num = int(choice)
        if 1 <= num <= 5:
            return choice
        print("Choice out of range. Please enter a number between 1 and 5.")


def get_book_details():
    """Prompt the user for book details and return them.

    This function interactively prompts the user for a book title, author, and
    optional publication year. The title is required and the function will
    re-prompt until a non-empty title is provided. The author may be left empty.

    Important behavior:
    - The publication year is optional. Blank or invalid year input is treated
      as a legacy "unknown" value represented by the integer 0 for
      compatibility with existing sample data and tests. In these cases the
      function prints a short warning and returns 0 for the year.

    Parameters:
        None

    Returns:
        tuple[str, str, int]: A tuple of (title, author, year) where `title` and
        `author` are strings and `year` is an int. A year value of 0 indicates
        an unknown/unspecified year (legacy representation).

    Side effects:
        Uses input() to read from stdin and prints messages to stdout when
        re-prompting for the title or when the year input is missing/invalid.
    """
    # Require a non-empty title; re-prompt until provided.
=======
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        print("Invalid choice. Please enter a number between 1 and 5.")


def get_book_details():
>>>>>>> origin/main
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print("Title cannot be empty. Please enter a title.")
    author = input("Enter author: ").strip()

    # Prompt for optional publication year; treat blank or invalid input as legacy 0.
    year_input = input("Enter publication year (optional): ").strip()
    if year_input == "":
        # Blank year treated as legacy 0 for compatibility with sample data/tests
        print("Invalid year. Enter digits only, or press Enter to leave blank.")
        year = 0
    else:
        try:
            year = int(year_input)
        except ValueError:
            print("Invalid year. Enter digits only, or press Enter to leave blank.")
            year = 0

    return title, author, year


def print_books(books):
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        year = str(book.year) if getattr(book, "year", None) not in (None, 0) else "Unknown"
        print(f"{index}. {book.title} by {book.author} ({year}) - {status}")
