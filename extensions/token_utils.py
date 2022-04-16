import datetime
import jwt
from flask import jsonify, redirect, request
from os import getenv
from functools import wraps


def jwt_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        token = request.header.get('Authorization').split()[-1]

        try:
            jwt.decode(
                token,
                getenv('JWT_SECRET'),
                algorithms=['HS256']
            )
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({
                'ACK': False,
                'mensagem': 'Token expirado'
            })
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({
                'ACK': False,
                'mensagem': 'Token inválido'
            })
        except jwt.exceptions.DecodeError:
            return jsonify({
                'ACK': False,
                'mensagem': 'Token inválido'
            })
        except Exception as e:
            return jsonify({
                'ACK': False,
                'mensagem': f'erro: {e}'
            })
        return fn(*args, **kwargs)

    return wrapped()


def refresh_token_required(fn):
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')

        try:
            jwt.decode(
                token,
                getenv('JWT_REFRESH_SECRET'),
                algorithms=['HS256']
            )
        except jwt.exceptions.ExpiredSignatureError:
            return redirect("/login")
        except Exception as e:
            return jsonify({
                'ACK': False,
                'mensagem': f'erro: {e}'
            })
        return fn(*args, **kwargs)

    return decorated_function


def generate_access_token(user_id):
    return jwt.encode(
        {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        },
        getenv('JWT_SECRET'),
        algorithm='HS256'
    )


def generate_refresh_token(user_id):
    return jwt.encode(
        {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
        },
        getenv('JWT_REFRESH_SECRET'),
        algorithm='HS256'
    )
