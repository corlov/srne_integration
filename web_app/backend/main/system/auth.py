from flask import Blueprint
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import jwt
import datetime
import time
import json
import uuid
import os
import bcrypt
import psycopg2
from psycopg2 import sql
import psycopg2.extras
# local modules:
import common.db as db
import common.glb_consts as glb
import common.inmemory as im
import common.utils as u



auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/login', methods=['POST'])
def login():
    users = db.load_users()

    data = request.json
    username = data.get('username')
    password = data.get('password', '')

    if username is None or password == '':
        return jsonify(message='Missing credentials'), 400

    password_bytes = password.encode('utf-8')

    user = next((u for u in users if u['username'] == username), None)
    if not user or not user.get('hashed_password'):
        return jsonify(message='Invalid credentials'), 401

    # ensure hashed_password is bytes
    stored = user['hashed_password']
    print(stored)
    if isinstance(stored, str):
        stored = stored.encode('utf-8')

    try:
        if bcrypt.checkpw(password_bytes, stored):
            token = jwt.encode({
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=glb.EXP_LIMIT),
                'role': user.get('role')
            }, glb.SECRET_KEY)
            db.event_log_add(f'Вход пользователя {username}', 'login', 'EVENT', 'INFO')
            return jsonify(token=token)
    except Exception:
        return jsonify(message='Exception'), 401
    return jsonify(message='Invalid credentials'), 401