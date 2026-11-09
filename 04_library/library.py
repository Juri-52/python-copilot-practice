from book import Book
from member import Member


class Library:
    def __init__(self, books: list[Book], members: list[Member]):
        self.books = books
        self.members = members

    def find_book(self, book_id: int) -> Book:
        for book in self.books:
            if book.book_id == book_id:
                return book
        raise ValueError("本が見つかりません")

    def find_member(self, member_id: int) -> Member:
        for member in self.members:
            if member.member_id == member_id:
                return member
        raise ValueError("会員が見つかりません")

    def lend_book(self, book_id: int, member_id: int) -> None:
        member = self.find_member(member_id)
        book = self.find_book(book_id)
        if book.borrower_id is not None:
            raise ValueError("貸出中です")
        book.borrower_id = member.member_id

    def return_book(self, book_id: int, member_id: int) -> None:
        member = self.find_member(member_id)
        book = self.find_book(book_id)
        if book.borrower_id is None:
            raise ValueError("この本は貸し出されていません")
        if book.borrower_id != member.member_id:
            raise ValueError("借りた会員と一致しません")
        book.borrower_id = None
