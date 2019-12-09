# from flask import *
from flask import Flask, request, jsonify, render_template,make_response, session
from service import ToDoService
from models import Schema
import json,requests
from urllib import parse
from datetime import datetime, timedelta 
from http import cookies


# app = Flask(__name__)
app = Flask(__name__, template_folder='templates')


# @app.after_request
# def add_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
#     response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
#     return response


# @app.route("/add")
# def addData():
#     requests.post("http://localhost:8888/todo", json={"Title":"my second todo", "Description":"my second todo"})
#     return 'inserted successfully'


# # http://127.0.0.1:8888/del/4
# @app.route("/del/<item_id>")
# def delData(item_id):
#     requests.delete("http://localhost:8888/todo/"+item_id)
#     return 'deleted successfully'



# # http://127.0.0.1:8888/edit/4
# @app.route("/edit/<item_id>")
# def updateData(item_id):
#     requests.put("http://localhost:8888/todo/"+item_id, json={"Title":"my new todo", "Description":"my new todo"})
#     return 'Updated successfully'


# @app.route('/test')
# def index():
#     return render_template('index.html')

@app.route('/login', methods=["POST"])
def login():
    if request.method=='POST':
        result = request.form      
        return render_template('success.html', result=result)
    else:
        return render_template('success.html', name='wrong method type')

@app.route("/todo", methods=["GET"])
def list_todo():
    return jsonify(ToDoService().list())


@app.route("/todo", methods=["POST"])
def create_todo():
    return jsonify(ToDoService().create(request.get_json()))


@app.route("/todo/<item_id>", methods=["PUT"])
def update_item(item_id):
    return jsonify(ToDoService().update(item_id, request.get_json()))


@app.route("/todo/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    return jsonify(ToDoService().delete(item_id))

@app.route('/')
def index():
    dayCheck = 1000
    json_data = fetch_offerlist()
    if json_data is not None:
        resp = make_response(render_template('success.html', json_data = json_data, dayCheck= dayCheck))
        resp.set_cookie('API Provider', 'Affise')# setting cookie data
        return resp
    else:
        return 'Something went wrong with api call.'


@app.route('/getCookie/')
def get_cookie():
    username = request.cookies.get('userCook')
    return username

@app.route('/setSess/')
def setSess():
    session.pop('name',None) # delete session data 
    session['email'] = 'email#1@gmail.com'  
    return render_template('cookie-session.html')


def fetch_offerlist():
    x = datetime.now()
    today = x.strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    payload = {}
    payload['limit'] = '500'
    payload['filter[date_from]'] = yesterday
    payload['filter[date_to]'] = today
    payload['slice[0]'] = 'offer'
    payload['orderType'] = 'desc'  
    payload['order[0]'] = 'raw' 
    payload['page'] = 1
    endpoint = 'http://api.xapads.affise.com/3.0/stats/custom'
    if payload is not None:
      url = endpoint + '?' + parse.urlencode(payload)
    response = requests.get(url, headers={'API-Key': 'e07d9cae9b1d6191e29b7597c59b837ce2fb784c'}) 
    
    json_data = response.json() if response and response.status_code == 200 else None
    return json_data
    






if __name__ == "__main__":
    Schema()
    app.secret_key = '$$this#is#my#secret#key$$'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, port=8888)
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms