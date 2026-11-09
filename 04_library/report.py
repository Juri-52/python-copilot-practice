from library import Library


def build_report(library: Library) -> str:
    lines = ["図書館の本:"]
    for book in library.books:
        if book.borrower_id is None:
            lines.append(f"{book.book_id}: {book.title} [貸出可能]")
        else:
            member = library.find_member(book.borrower_id)
            lines.append(f"{book.book_id}: {book.title} [貸出中: {member.name}]")
    return "\n".join(lines)
