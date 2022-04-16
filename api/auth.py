from os import getenv
from flask import Blueprint, jsonify, request
from extensions.token_utils import generate_refresh_token, refresh_token_required, generate_access_token
from extensions.db import get_conn

blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='/api/v1'
)

@blueprint.route("/auth/get_access_token")
@refresh_token_required
def get_access_token():
    return jsonify(
        {
            'token': generate_access_token(
        request.cookies.get('user_id'))
        }
    )


@blueprint.route("/auth", methods=['POST'])
def auth():
    username = request.json.get('username')
    password = request.json.get('password')

    db = get_conn('user')

    try:
        user = [
            {
                'username': u.get('username'),
                'password': u.get('password')
            } for u in db.users.find({'username': username})
        ]

        credentialIsValid = username == user[0].get('username') and password == user[0].get('password')



    except IndexError:
        return jsonify({
            'ACK': False,
            'message': "usuário ou senha inválidos"
        })

    if credentialIsValid:
        return jsonify(
            {
                'ACK': True,
                'token': generate_refresh_token(username)
            }
        )
    return jsonify({
        'ACK': False,
        'message': "usuário ou senha inválidos"
    })
