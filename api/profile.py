from flask import Blueprint, jsonify, request
from extensions.db import get_conn
from extensions.token_utils import (jwt_required)

blueprint = Blueprint("profile", __name__, url_prefix="api/v1")


@blueprint.route("/get_profile_data", methods=["POST"])
@jwt_required
def get_profile_data():
    db = get_conn('user')
    user_id = request.json.get('user_id')

    try:
        profile_data = [
            {
                'full_name': u['profile']['full_name'],
                'profile': u['profile']['profile'],
                'email': u['profile'],
                'registration_date': u['profile']['registration_date']
            } for u in db.users.find({'username': user_id})
        ]

    except Exception as e:
        return jsonify(
            {
                'ACK': False,
                'message': (f'deu erro no profile:', e.__str__())
            }
        )
    return jsonify(profile_data[0])
