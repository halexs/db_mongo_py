from flask import Flask, redirect, url_for, request, render_template
from flask.json import jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(
    'mongodb',
    #localhost,
    27017)
#db = client.tododb
db = client.servers
collection = db.machines
#server_list_all = query_all(None)

@app.route('/')
def hello():
    return "Flask inside Docker!!"

@app.route('/todo')
def todo():

    #_items = db.machines.find({'child'})
    query1 = {'child':{'$exists':True}}
    query2 = None
    items = query_all(query1)
    #items = server_list_all
    l = list(items)
    js = jsonify(l)
    return str(l)

@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.machines.insert_one(item_doc)

    return redirect(url_for('todo'))

def query_all(query):
    _items = db.machines.find(query)
    items = [item for item in _items]
    return items

def query_one(query_id):
    _items = db.machines.find_one({'_id':query_id})
    #items = [item for item in _items]
    return _items

# Takes a dictionary list that was from mongodb and makes the dereferences the data to point to the write id.
# Does this process by iterating through a list and adding the element to the parent.
def dereference(machine_dict):
    new_list = []
    substitute(machine_dict)
    for machine in machine_dict:
        if "child" in machine:
            deref = []
            for child in machine['child']:
                child_ele = query(child)
                deref.append(child_ele)
            return None
        #if "parent" in item:
        #    par_id = item["parent"]
        #    cur_id = item["_id"]

        #    return None
        #else:
        #    new_list.append(item)
    return machine_dict

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

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