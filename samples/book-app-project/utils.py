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
        if not choice:
            print("Please enter a choice (1-5).")
            continue
        if not choice.isdigit():
            print("Invalid input. Please enter a number between 1 and 5.")
            continue
        num = int(choice)
        if 1 <= num <= 5:
            return choice
        print("Choice out of range. Please enter a number between 1 and 5.")


def get_book_details():
    """Prompt the user for book details and return them.

    This function interactively prompts the user for a book title, author, and
    publication year. The title is required and the function will re-prompt
    until a non-empty title is provided. The author may be left empty.
    The publication year is converted to an integer; if conversion fails the
    function prints a message and defaults the year to 0.

    Parameters:
        None

    Returns:
        tuple[str, str, int]: A tuple of (title, author, year) where `title` and
        `author` are strings and `year` is an int.

    Side effects:
        Uses input() to read from stdin and prints messages to stdout when
        re-prompting for the title or when the year input is invalid.
    """
    # Require a non-empty title; re-prompt until provided.
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print("Title cannot be empty. Please enter a title.")
    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books):
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
