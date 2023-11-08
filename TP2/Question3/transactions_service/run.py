from users_service import app, db
from users_service.models.available_ids import AvailableIDs
from users_service.models.user import User


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
