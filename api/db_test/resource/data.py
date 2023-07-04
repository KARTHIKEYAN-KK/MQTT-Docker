from flask import Flask, request, Response, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import DataSchema, DataUpdateSchema
import pytz
from datetime import datetime
import json
from db import conn

india = pytz.timezone('Asia/Kolkata')
blp = Blueprint("Energy Data", __name__, description="Operations on Energy data")

@blp.route("/alldata")
class DataList(MethodView):
    @blp.response(200, DataSchema(many=True))
    def get(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM test_table")
        data = cur.fetchall()
        result = []
        temp = {}
        for value in data:
            temp = {'time':value[3], 'volt_01':value[0], 'volt_02':value[1], 'volt_03':value[2]
            }
            result.append(temp)
            temp = {}
        return jsonify(result)
        


@blp.route("/data")
class Data(MethodView):
    @blp.response(200, DataSchema)
    def get(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM test_table ORDER BY id DESC LIMIT 1")
        data = cur.fetchone()
        if len(data) == 0:
            return jsonify({'message': 'No data found'})
        result ={}
        result["time"] = data[3]
        result["volt_01"] = data[0]
        result["volt_02"] = data[1]
        result["volt_03"] = data[2]
        return jsonify(result)

    @blp.arguments(DataSchema)
    @blp.response(201, DataSchema)
    def post(self, json_data):
        json_data = request.get_json()
        v1 = json_data['v1']
        v2 = json_data['v2']
        v3 = json_data['v3']
        # Get the current UTC time
        utc_time = datetime.utcnow()
        # Convert UTC time to IST
        ist_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Kolkata"))
        cur = conn.cursor()
        cur.execute("INSERT INTO test_table (v1, v2, v3, time) VALUES (%s, %s, %s, %s)", (v1, v2, v3, ist_time))
        conn.commit()
        return jsonify({
            "message":"Data inserted succefully"
        })



@blp.route("/data_by/<int:interval>")
class DataInterval(MethodView):
    @blp.response(200, DataSchema(many=True))
    def get(self, interval):
        cur = conn.cursor()
        cur.execute("SELECT * FROM test_table WHERE time >= NOW() - INTERVAL '%s' MINUTE", (interval,))
        data = cur.fetchall()
        if len(data) == 0:
            return jsonify({'message': 'No data found'})
        result = []
        temp = {}
        for value in data:
            temp = {'time':value[3], 'volt_01':value[0], 'volt_02':value[1], 'volt_03':value[2]
            }
            result.append(temp)
            temp = {}
        return jsonify(result)

@blp.route("/esp/data")
class DataForTesting(MethodView):
    data = {
        "data": "start#SuperZIG23#4#false#104#90#true#true"
        }

    def get(self):
        return self.data

    def put(self):
        updated_data = request.json
        self.data.update(updated_data)

        return {"message": "Data updated successfully."}