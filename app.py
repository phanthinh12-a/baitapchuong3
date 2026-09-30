from flask import Flask, jsonify, request, url_for
from markupsafe import escape
from data import BOOKS

app = Flask(__name__)


# Trang chủ
@app.route("/")
def home():
    total = len(BOOKS)

    available = sum(
        1 for book in BOOKS
        if book["available"]
    )

    return f"""
    <h1>LibraryMS v0.1</h1>

    <p>Tổng số đầu sách: {total}</p>
    <p>Số sách sẵn sàng cho mượn: {available}</p>

    <a href="{url_for('books')}">
        Xem danh sách sách
    </a>
    """


# Danh sách sách + lọc theo category
@app.route("/books")
def books():
    category = request.args.get("category", "").strip()

    if category:
        result = [
            book for book in BOOKS
            if book["category"].lower() == category.lower()
        ]
    else:
        result = BOOKS

    html = """
    <h1>Danh sách sách</h1>

    <table border="1" cellpadding="8">
        <tr>
            <th>ID</th>
            <th>Tên sách</th>
            <th>Tác giả</th>
            <th>Năm</th>
            <th>Thể loại</th>
            <th>Trạng thái</th>
        </tr>
    """

    for book in result:
        status = (
            "Sẵn sàng"
            if book["available"]
            else "Đang được mượn"
        )

        html += f"""
        <tr>
            <td>{escape(book["id"])}</td>

            <td>
                <a href="{url_for(
                    'book_detail',
                    book_id=book['id']
                )}">
                    {escape(book["title"])}
                </a>
            </td>

            <td>{escape(book["author"])}</td>
            <td>{escape(book["year"])}</td>
            <td>{escape(book["category"])}</td>
            <td>{escape(status)}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/">Về trang chủ</a>
    """

    return html


# Chi tiết sách
@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = next(
        (book for book in BOOKS if book["id"] == book_id),
        None
    )

    if book is None:
        return f"""
        <h1>404 - Không có sách với ID = {escape(book_id)}</h1>

        <a href="{url_for('books')}">
            Quay lại danh sách
        </a>
        """, 404

    status = (
        "Sẵn sàng cho mượn"
        if book["available"]
        else "Đang được mượn"
    )

    return f"""
    <h1>Chi tiết sách</h1>

    <p><b>ID:</b> {escape(book["id"])}</p>
    <p><b>Tên sách:</b> {escape(book["title"])}</p>
    <p><b>Tác giả:</b> {escape(book["author"])}</p>
    <p><b>Năm:</b> {escape(book["year"])}</p>
    <p><b>Thể loại:</b> {escape(book["category"])}</p>
    <p><b>Trạng thái:</b> {escape(status)}</p>

    <a href="{url_for('books')}">
        Quay lại danh sách
    </a>
    """


# API danh sách sách
@app.route("/api/books")
def api_books():
    return jsonify(BOOKS)


# API chi tiết sách
@app.route("/api/books/<int:book_id>")
def api_book_detail(book_id):
    book = next(
        (book for book in BOOKS if book["id"] == book_id),
        None
    )

    if book is None:
        return jsonify({
            "error": f"Không có sách với ID = {book_id}"
        }), 404

    return jsonify(book)


# Trang 404 dùng chung
@app.errorhandler(404)
def not_found(error):
    return """
    <h1>404 - Không tìm thấy</h1>

    <p>Trang bạn yêu cầu không tồn tại.</p>

    <a href="/">Về trang chủ</a>
    """, 404


if __name__ == "__main__":
    app.run(debug=True)