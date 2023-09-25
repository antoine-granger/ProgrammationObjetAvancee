from transactions_service import app, db
from transactions_service.models.available_ids import AvailableIDs
from transactions_service.models.transaction import Transaction


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
