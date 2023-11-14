from time import sleep

from books_service import app, db
from books_service.models.available_ids import AvailableIDs
from books_service.models.book import Book


if __name__ == '__main__':
    sleep(60)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
