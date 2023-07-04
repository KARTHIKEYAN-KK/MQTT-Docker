from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import UserModel
from schemas import UserSchema, UserLoginSchema, UserDetailsSchema
from passlib.hash import pbkdf2_sha256

blp = Blueprint("Users", "users", description="Operation on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="A user with that email already exists.")

        user = UserModel(
            name=user_data["name"],
            email=user_data["email"],
            phoneNumber=user_data["phoneNumber"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/api/userDetails/<string:user_id>")
class UserDetails(MethodView):
    def get(self, user_id):
        user = UserModel.query.filter(UserModel.id == user_id).first()

        if user:
            return {
                "user_id": user.id,
                "status": user.status,
                "role": user.role,
                "phoneNumber": user.phoneNumber,
            }, 200

        abort(401, message="Invalid credentials.")


@blp.route("/api/getUserDetails/<string:user_id>")
class getUserDetails(MethodView):
    @blp.response(200, UserDetailsSchema(many=True))
    def get(self, user_id):
        user = UserModel.query.filter(UserModel.id == user_id).first()
        if user.role == 3:
            return UserModel.query.all()

        abort(401, message="Invalid credentials.")


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.phoneNumber == user_data["phoneNumber"]).first()
        if user:
            if user and pbkdf2_sha256.verify(user_data["password"], user.password):
                return {
                    "user_id": user.id,
                    "status": user.status,
                    "role": user.role,
                    "phoneNumber": user.phoneNumber,
                    "username": user.name
                }, 200

            abort(401, message="Invalid credentials.")
        else:
            abort(404, message="No user found.")