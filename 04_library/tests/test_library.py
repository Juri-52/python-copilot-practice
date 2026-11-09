import pytest

from book import Book
from library import Library
from member import Member


def test_lend_then_return_updates_same_book():
    book = Book(1, "Python入門")
    library = Library([book], [Member(1, "田中")])

    library.lend_book(1, 1)
    assert book.borrower_id == 1
    assert library.books[0] is book

    library.return_book(1, 1)
    assert book.borrower_id is None


def test_second_loan_preserves_original_borrower():
    book = Book(1, "Python入門")
    library = Library([book], [Member(1, "田中"), Member(2, "佐藤")])
    library.lend_book(1, 1)

    with pytest.raises(ValueError) as error:
        library.lend_book(1, 2)

    assert str(error.value) == "貸出中です"
    assert book.borrower_id == 1


def test_other_member_cannot_return_book():
    book = Book(1, "Python入門")
    library = Library([book], [Member(1, "田中"), Member(2, "佐藤")])
    library.lend_book(1, 1)

    with pytest.raises(ValueError) as error:
        library.return_book(1, 2)

    assert str(error.value) == "借りた会員と一致しません"
    assert book.borrower_id == 1


def test_unknown_member_id_raises_member_error():
    library = Library([Book(1, "Python入門")], [Member(1, "田中")])

    with pytest.raises(ValueError) as error:
        library.lend_book(1, 999)

    assert str(error.value) == "会員が見つかりません"


def test_unknown_book_id_raises_book_error():
    library = Library([Book(1, "Python入門")], [Member(1, "田中")])

    with pytest.raises(ValueError) as error:
        library.lend_book(999, 1)

    assert str(error.value) == "本が見つかりません"


def test_unknown_member_error_takes_priority_when_both_ids_are_unknown():
    library = Library([Book(1, "Python入門")], [Member(1, "田中")])

    with pytest.raises(ValueError) as error:
        library.lend_book(999, 999)

    assert str(error.value) == "会員が見つかりません"


def test_returning_unborrowed_book_raises_error_without_changing_state():
    book = Book(1, "Python入門")
    library = Library([book], [Member(1, "田中")])

    with pytest.raises(ValueError) as error:
        library.return_book(1, 1)

    assert str(error.value) == "この本は貸し出されていません"
    assert book.borrower_id is None


def test_find_methods_return_original_objects():
    book = Book(1, "Python入門")
    member = Member(1, "田中")
    library = Library([book], [member])

    assert library.find_book(1) is book
    assert library.find_member(1) is member
