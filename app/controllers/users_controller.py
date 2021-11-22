from app import app
from app.entities import User

@app.route("/api/v1/users", methods = ["GET"])
def get_all_user():
    pass

@app.route("/api/v1/users/<int:user_id", methods = ["GET"])
def get_user(user_id):
    pass

@app.route("/api/v1/users", methods = ["POST"])
def create_user():
    pass

@app.route("/api/v1/users/<int:user_id>", methods = ["PUT"])
def update_user(user_id):
    pass

@app.route("/api/v1/users/<int:userId>", methods = ["DELETE"])
def delete_user(user_id):
    pass

@app.route("/api/v1/delete-users", methods = ["POST"])
def delete_multiple_users():
    pass

@app.route("/api/v1/users/auth", methods = ["POST"])
def auth_user():
    pass

@app.route("/api/v1/users/register", methods = ["POST"])
def register_user():
    pass