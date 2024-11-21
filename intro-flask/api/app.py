from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
# Ganti dengan kredensial MySQL Anda
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/myflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from routes import *
if __name__ == "__main__":
    app.run(debug=True)

    from flask_cors import CORS # Import Flask-CORS
    CORS(app) # Mengizinkan semua domain