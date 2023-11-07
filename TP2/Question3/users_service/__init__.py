from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# Importation des views
# import sys
# sys.path.append("C:/GitHub/ProgrammationObjetAvancee/TP2/Question3/users_service")
from views import user_views