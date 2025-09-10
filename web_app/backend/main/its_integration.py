

# Возможно пригодиться при REST API?
# @app.route('/dynamic_data', methods=['GET'])
# def dynamic_data_get():
#     error = u.check_auth(request.args.get('Authorization'))
#     if error:
#         return error

#     device_id = request.args.get('deviceId')
#     return im.redis_read_json(im.RK_TELEMETRY, device_id)


# @app.route('/system_info', methods=['GET'])
# def system_info():
#     error = u.check_auth(request.args.get('Authorization'))
#     if error:
#         return error

#     device_id = request.args.get('deviceId')
#     sys_list = im.redis_read_json(im.RK_SYS_INFO, device_id)
#     res_hash = {}
#     for s in sys_list:
#         for key, value in s.items():
#             if key != 'unit':
#                 res_hash[key] = value
    
#     return res_hash

# более защищенный вариант
# @app.route('/system_info', methods=['GET'])
# def system_info():
#     # Prefer header auth
#     auth_header = request.headers.get('Authorization')
#     if not auth_header:
#         return jsonify(message='Missing authorization'), 401

#     error = u.check_auth(auth_header)
#     if error:
#         return error

#     device_id = request.args.get('deviceId')
#     if not device_id or not isinstance(device_id, str) or len(device_id) > 64:
#         return jsonify(message='Invalid deviceId'), 400
#     # optional: validate allowed chars
#     if not re.match(r'^[A-Za-z0-9_\-]+$', device_id):
#         return jsonify(message='Invalid deviceId'), 400

#     # authorization: ensure current user can access this device
#     current_user = u.get_current_user()  # adapt to your auth API
#     if not current_user.is_admin and not u.user_has_device(current_user, device_id):
#         return jsonify(message='Forbidden'), 403

#     try:
#         sys_list = im.redis_read_json(im.RK_SYS_INFO, device_id)
#     except Exception as ex:
#         app.logger.exception('Redis read error')
#         return jsonify(message='Internal error'), 500

#     if not sys_list:
#         return jsonify({}), 200

#     res_hash = {}
#     for s in sys_list:
#         if not isinstance(s, dict):
#             continue
#         for key, value in s.items():
#             if key == 'unit':
#                 continue
#             # optionally limit key/value sizes/types
#             res_hash[str(key)] = value

#     # limit response size
#     if len(res_hash) > 1000:
#         return jsonify(message='Response too large'), 413

#     return jsonify(res_hash)



# # настройки контроллера СП
# @app.route('/settings', methods=['GET'])
# def settings():
#     token = request.headers.get('Authorization')
        
#     if not token:
#         return jsonify(message='Token is missing!')

#     try:
#         data = jwt.decode(token, glb.SECRET_KEY, algorithms=["HS256"])
#         print("Hello, ", data['username'])
        
#         device_id = request.args.get('deviceId')
#         return im.redis_read_json(im.RK_SETTINGS, device_id)    
#     except jwt.ExpiredSignatureError:
#         return jsonify(message='Token has expired!')
#     except jwt.InvalidTokenError:
#         return jsonify(message='Invalid token!')




# # настройки всего комплекса
# @app.route('/complex_settings', methods=['GET'])
# def complex_settings():
#     # FIXME: в настройки пароли убрать
#     connection_params = {
#         'host': 'localhost',
#         'database': 'solar_controller_telemetry',
#         'user': 'postgres',
#         'password': 'gen_postgress_password',
#         'port': '5432'
#     }

#     try:
#         conn = psycopg2.connect(**connection_params)
#         cursor = conn.cursor()
#         query = sql.SQL("SELECT param, value FROM solar_controller_telemetry.device.complex_settings")
#         cursor.execute(query)        
#         rows = cursor.fetchall()
#         result_dict = {key: value for key, value in rows}
        
#         return result_dict

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()
    
#     return {}