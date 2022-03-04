from api import app, db
from flask_sqlalchemy import SQLAlchemy, get_debug_queries

if __name__ == "__main__":
    app["SQLALCHEMY_RECORD_QUERIES"] = True
    db.create_all()
    info = get_debug_queries()
    print(info)