from flask import jsonify
import jwt
import json
import datetime
import re
import uuid

import common.db as db
import common.glb_consts as glb
import common.inmemory as im



def check_auth(token):
    if not token:
        return jsonify(message='Token is missing!')

    try:
        data = jwt.decode(token, glb.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify(message=f'check_auth, Token has expired! {token}')
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


# Helper function to validate NTP server addresses
def is_valid_ntp_server(address):
    """Validate NTP server address format"""
    try:
        # Basic validation - extend based on your requirements
        if not address or len(address) > 253:
            return False
        
        # Check for IP address or valid hostname
        if re.match(r'^[\w\.\-]+$', address):
            return True
            
        return False
    except:
        return False



def create_controller_command(command_name):
    now = datetime.datetime.now()
    cmd = {}
    cmd['user'] = 'admin'
    cmd['command'] = command_name
    cmd['created_at'] = str(now.timestamp())
    cmd['uuid'] = str(uuid.uuid4())
    return cmd
