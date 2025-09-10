from flask import jsonify
import jwt
import json
import datetime

import common.db as db
import common.glb_consts as glb
import common.inmemory as im



def check_auth(token):
    if not token:
        return jsonify(message='Token is missing!')

    try:
        data = jwt.decode(token, glb.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token has expired!')
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token!')

    return None


def convert_dates(start_d, end_d):
    if not start_d:
        start_d = datetime.datetime.now().strftime('%Y-%m-%d')
    if not end_d:
        end_d = datetime.datetime.now().strftime('%Y-%m-%d')
    start_d = f"{start_d} 00:00:00"
    end_d   = f"{end_d} 23:59:59"

    return start_d, end_d