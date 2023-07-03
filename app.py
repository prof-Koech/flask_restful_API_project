from flask import Flask,request
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


db.init_app(app)
Migrate = Migrate(app,db)
api =Api(app)


class UserResource(Resource):
    def post(self):
        # fetching data from the request body
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Checking if the user  exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "User Exists!!"}, 400

        # Creating a new User 
        user = User(username=username, email=email)
        user.set_password(password)

        #add user to db
        db.session.add(user)
        db.session.commit()


        return {"message": "User successfully created "}, 201
    



    def get(self):
            users = User.query.all()
            data = [
                {"id": user.id, "username": user.username, "email": user.email}
                for user in users
            ]
            return data


class SingleUserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = {"id": user.id, "username": user.username, "email": user.email}
            return data
        else:
            return {"error": "User not found"}, 404

    def put(self, user_id):
        # Get the data from the request body
        data = request.get_json()

        # Check if the user exists 
        user = User.query.get(user_id)
        if user:
            # Update the user details
            user.username = data.get("username", user.username)
            user.email = data.get("email", user.email)
            db.session.commit()
            return {"message": "User updated successfully"}
        else:
            return {"error": "User not found"}, 404

    def patch(self, user_id):
        # Fetching data from the request body
        data = request.get_json()

        # Check if the user exists
        user = User.query.get(user_id)
        if user:
            # Update the user password 
            new_password = data.get("password")
            if new_password:
                user.set_password(new_password)

           
            if "username" in data:
                user.username = data["username"]
            if "email" in data:
                user.email = data["email"]

            db.session.commit()
            return {"message": "User updated successfully"}
        else:
            return {"error": "User not found"}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted from database"}
        else:
            return {"error": "User not found"}, 404


api.add_resource(UserResource, "/users")
api.add_resource(SingleUserResource, "/users/<int:user_id>")   

if __name__=="__main__":
    app.run(port=5555)