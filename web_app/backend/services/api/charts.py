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

import common.db as db
import common.glb_consts as glb
import common.inmemory as im
import common.utils as u


charts_bp = Blueprint('charts', __name__)



@charts_bp.route("/get_timeseries")
def controller_temp():
    """
    Query params:
      - range: e.g. '7d' (default) or '24h'
      - limit: max raw points when no downsample (optional)
    Returns JSON array: [{ "x": ISO8601, "y": int }, ...]
    """
    rng = request.args.get("range", "7d")
    limit = request.args.get("limit", type=int, default=10000)

    # parse range
    now = datetime.datetime.now(datetime.timezone.utc)
    if rng.endswith("d"):
        hours = int(rng[:-1]) * 24
    elif rng.endswith("h"):
        hours = int(rng[:-1])
    else:
        hours = 24 * 7
    start = now - datetime.timedelta(hours=hours)

    rows = db.get_timeseries_fro_charts()
  
    controller_temperature = [{"x": r["ts"], "y": r["controller_temperature"]} for r in rows]
    battery_temperature = [{"x": r["ts"], "y": r["battery_temperature"]} for r in rows]
    battery_volts = [{"x": r["ts"], "y": r["battery_volts"]} for r in rows]
    maxv = [{"x": r["ts"], "y": r["maxv"]} for r in rows]
    minv = [{"x": r["ts"], "y": r["minv"]} for r in rows]
    data = {
        'controller_temperature': controller_temperature,
        'battery_temperature': battery_temperature,
        'battery_volts': battery_volts,
        'maxv': maxv,
        'minv': minv
    }
    return jsonify(data)
