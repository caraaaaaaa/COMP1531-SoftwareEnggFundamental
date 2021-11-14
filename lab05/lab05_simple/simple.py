from flask import Flask, request
from json import dumps

app = Flask(__name__)

# Write your routes here
name_list = []

@app.route("/name/add", methods=['POST'])
def add_name():
    global name_list
    data = request.get_json()
    # if data['name'] in name_list:
    #     return {"status": 400, "msg": "Name already exist"}
    name_list.append(data['name'])
    return {}

@app.route("/names", methods=['GET'])
def names():
    global name_list
    return {'names':name_list}

@app.route("/name/remove", methods=['DELETE'])
def remove():
    global name_list
    data = request.get_json()
    name_list.remove(data['name'])
    return {}

if __name__ == '__main__':
    app.run(port=0)