from pprint import pprint
from flask import Flask, jsonify, request

from cache_service import CacheService
from models import Book, Topic
from replica_sync_service import ReplicaSyncService
from utils import session

app = Flask(__name__)


def initialize_db():
    # Check if DB is empty and fill it if so
    topics_count = session.query(Topic).count()
    books_count = session.query(Book).count()
    if topics_count == 0 and books_count == 0:
        # Creating topics
        distributed_systems = Topic(name="distributed systems")
        undergraduate_school = Topic(name="undergraduate school")
        session.add_all([distributed_systems, undergraduate_school])
        session.commit()

        # Creating books
        book_1 = Book(title="How to get a good grade in DOS in 40 minutes a day", price=10.99, quantity=15,
                      topic_id=distributed_systems.id)
        book_2 = Book(title="RPCs for Noobs", price=15.0, quantity=20, topic_id=distributed_systems.id)
        book_3 = Book(title="Xen and the Art of Surviving Undergraduate School", price=5.0, quantity=10,
                      topic_id=undergraduate_school.id)
        book_4 = Book(title="Cooking for the Impatient Undergrad", price=8.5, quantity=15,
                      topic_id=undergraduate_school.id)
        book_5 = Book(title="How to finish project 3 on time", price=8, quantity=15,
                      topic_id=distributed_systems.id)
        book_6 = Book(title="Why theory classes are so hard", price=9, quantity=20,
                      topic_id=undergraduate_school.id)
        book_7 = Book(title="Spring in pioneer valley", price=10, quantity=20,
                      topic_id=distributed_systems.id)
        session.add_all([book_1, book_2, book_3, book_4, book_5, book_6, book_7])
        session.commit()


initialize_db()


@app.route('/search/<topic>', methods=["GET"])
def search(topic):
    # get books with the specified topic
    books = session.query(Book).\
        join(Topic, Topic.id == Book.topic_id).\
        filter(Topic.name.ilike(topic)).all()
    # format response
    response = []
    for book in books:
        book_dict = {
            "id": book.id,
            "title": book.title
        }
        response.append(book_dict)

    # print response before sending it
    pprint(response)
    return jsonify(response)


@app.route('/info/<book_id>', methods=["GET"])
def info(book_id):
    # get the book with the requested id
    book = session.query(Book).\
        filter(Book.id == book_id).one_or_none()
    # check if book exists
    if book:
        response = {
            "title": book.title,
            "quantity": book.quantity,
            "price": book.price
        }
        # print response before sending it
        pprint(response)
        return jsonify(response)
    else:
        # return no book found error if book does not exist
        print("No book was found")
        return jsonify({"error": "No book found."})


@app.route('/update/<book_id>', methods=["PUT"])
def update(book_id):
    # get the book with the requested id
    request_body = request.json
    book = session.query(Book).\
        filter(Book.id == book_id).one_or_none()
    # check if book exists
    if book:
        book = session.query(Book). \
            filter(Book.id == book_id).\
            update(request_body)
        CacheService().remove_book_cache(book_id=book_id)
        session.commit()
        ReplicaSyncService().sync_book(book_id=book_id, request_data=request_body)
        return jsonify({"message": "Book updated successfully"})

    else:
        # return no book found error if book does not exist
        print("No book was found")
        return jsonify({"error": "No book found."})


@app.route('/sync/<book_id>', methods=["POST"])
def sync(book_id):
    request_body = request.json
    session.query(Book). \
        filter(Book.id == book_id). \
        update(request_body)
    session.commit()
    return jsonify({"message": "success"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')