from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(
    'mongodb',
    #localhost,
    27017)
#db = client.tododb
db = client.servers
collection = db.machines

@app.route('/')
def hello():
    return "Flask inside Docker!!"

@app.route('/todo')
def todo():

    _items = db.machines.find()
    items = [item for item in _items]
    #print(items)
    #return "finished accessing db"
    return render_template('todo.html', items=items)

@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.machines.insert_one(item_doc)

    return redirect(url_for('todo'))
'''

def todo():

    _items = db.servers.find()
    items = [item for item in _items]

    return render_template('todo.html', items=items)

@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))
'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)