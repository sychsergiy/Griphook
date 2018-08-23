from flask import jsonify, request
from flask.views import MethodView

from flask_jwt_extended import create_access_token

from .utils import get_admin


# TODO: set JWT_SECRET_KEY
# to use jwt_required()
class LoginView(MethodView):
    """
        Class manages login procedure

        Accepts json data as POST request:
        {
            "password": "johndoe"
        }

        If successful login - returns Json Web Token (JWT) in json:
        {
            "access_token": "**JWT TOKEN**"
        }
    """

    def post(self):
        if not request.is_json:
            return "Bad Request", 400

        password = request.json.get("password")

        # Check password field is filled
        if not password:
            return "Password field is unfilled", 400

        admin = get_admin()
        if not admin or not admin.check_password(password):
            return "Wrong password", 401

        # Create JWT and return it
        return (
            jsonify({"access_token": create_access_token(identity=admin.id)}),
            200,
        )
