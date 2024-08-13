#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from ipdb import set_trace

from config import app, db, api
from models import User, Recipe


class Signup(Resource):
    def post(self):
        try:
            data = request.json
            new_user = User(**data)
            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = new_user.id
            return make_response(new_user.to_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 422)


class CheckSession(Resource):
    def get(self):
        try:
            user_id = session.get('user_id')
            user = db.session.get(User, user_id)
            return make_response(user.to_dict(), 200)
        except Exception as e:
            return make_response({'error' : str(e)}, 401)


class Login(Resource):
    pass


class Logout(Resource):
    pass


class RecipeIndex(Resource):
    pass


api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(RecipeIndex, "/recipes", endpoint="recipes")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
