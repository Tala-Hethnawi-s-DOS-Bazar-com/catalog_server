from flask import Flask
from models import Book, Topic
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
        book_1 = Book(name="How to get a good grade in DOS in 40 minutes a day", price=10.99, in_stock_count=3,
                      topic_id=distributed_systems.id)
        book_2 = Book(name="RPCs for Noobs", price=15.0, in_stock_count=2, topic_id=distributed_systems.id)
        book_3 = Book(name="Xen and the Art of Surviving Undergraduate School", price=5.0, in_stock_count=10,
                      topic_id=undergraduate_school.id)
        book_4 = Book(name="Cooking for the Impatient Undergrad", price=8.5, in_stock_count=15,
                      topic_id=undergraduate_school.id)
        session.add_all([book_1, book_2, book_3, book_4])
        session.commit()


initialize_db()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
