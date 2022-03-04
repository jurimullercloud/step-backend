from api import db

if __name__ == "__main__":
    init_complete = False

    while not init_complete:
        try:
            db.create_all()
        except Exception as ex:
            print("Database has not found yet")
