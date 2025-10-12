from flask import Blueprint
from flask import Flask, request, jsonify, Response, g
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
from decorators import auth_required
import re

import common.db as db
import common.glb_consts as glb
import common.inmemory as im
import common.utils as u



auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        users = db.load_users()

        data = request.json
        username = data.get('username')
        password = data.get('password', '')

        if username is None or password == '':
            return jsonify(message='Missing credentials'), 400

        if users is None:
            return jsonify(message='Users empty'), 400

        password_bytes = password.encode('utf-8')

        user = next((u for u in users if u['username'] == username), None)
        if not user or not user.get('hashed_password'):
            return jsonify(message='Invalid credentials'), 401

        # ensure hashed_password is bytes
        stored = user['hashed_password']
        print(stored)
        if isinstance(stored, str):
            stored = stored.encode('utf-8')
    except Exception as e:
        return jsonify(message=f'Exception (stage 1): {e}, username: {username} password: {password}'), 401

    try:
        if bcrypt.checkpw(password_bytes, stored):
            token = jwt.encode({
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=glb.EXP_LIMIT),
                'role': user.get('role')
            }, glb.SECRET_KEY)
            db.event_log_add(f'Вход пользователя {username}', 'login', 'EVENT', 'INFO')
            return jsonify(token=token, exp=glb.EXP_LIMIT, role=user.get('role'))
    except Exception as e:
        return jsonify(message=f'Exception (stage 2): {e}'), 401

    return jsonify(message='Invalid credentials'), 401


def is_username_valid(username):
    # Define a regex pattern for valid characters
    pattern = r'^[a-zA-Z0-9_]+$'  # Only allows letters, digits, and underscores

    # Check if the username matches the pattern
    if re.match(pattern, username):
        return True
    else:
        return False



@auth_bp.route('/upsert_user', methods=['GET'])
@auth_required
def create_user():
    if g.token_data.get('role') not in ['operator', 'admin']:
        return jsonify(message='permission denied'), 401

    username = request.args.get("username")
    if not is_username_valid(username):
        return jsonify(message='incorrect username'), 401

    password = request.args.get("password")
    rolename = request.args.get("role")

    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    err_text = db.upsert_user(username, hashed_password, rolename)
    if err_text:
        return jsonify(message=err_text), 401
    
    return jsonify(message='OK'), 200
