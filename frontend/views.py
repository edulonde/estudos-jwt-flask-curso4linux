import requests
from os import getenv
from flask import Blueprint, render_template, request, make_response, redirect, jsonify
from extensions.token_utils import refresh_token_required

blueprint = Blueprint('views', __name__)


@blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        payload = {
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }

        resposta = None
        try:
            resposta = requests.post(f"{getenv('APP_URL')}/api/v1/auth",
                                     json=payload)
            refresh_token = resposta.json()

        except Exception as e:
            return jsonify({
                'ACK': False,
                'message': (f'deu erro na views:', e.__str__())
            })

        if refresh_token['ACK']:
            response = make_response(redirect("/profile"))
            response.set_cookie(key='token', value=refresh_token.get('token'), httponly=True)
            response.set_cookie(key='user_id', value=payload.get('username'), httponly=True)
            return response

    return render_template('login.html')


@blueprint.route("/profile")
@refresh_token_required
def get_profile():
    # return jsonify({
    #     'user_id': request.cookies.get('user_id'),
    #     'token': request.cookies.get('token')
    # })
    try:
        access_token = requests.get(f"{getenv('APP_URL')}/api/v1/auth/get_access_token",
                                 cookies=request.cookies)
        access_token = access_token.json()

    except Exception as e:
        return jsonify({
            'ACK': False,
            'message': (f'deu erro na views:', e.__str__())
        })

    return jsonify(access_token)