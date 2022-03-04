from api import app
from flask_sqlalchemy import SQLAlchemy

if __name__ == "__main__":
    init_complete = False

    while not init_complete:
        try:
            db = SQLAlchemy(app)
            db.create_all()
            init_complete = True
        except Exception as e:
            print("Database has not been created yet")