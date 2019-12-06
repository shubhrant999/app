from flask import Flask, request, jsonify, render_template
from service import ToDoService
from models import Schema

import json,requests

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST"])
def login():
    if request.method=='POST':
        name = request.form['name']
        password = request.form['pwd']
        mydic = {name,password}
        return render_template('success.html', data=mydic)
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


if __name__ == "__main__":
    Schema()
    app.run(debug=True, port=8888)
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms