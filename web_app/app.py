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
server_list_all = []

@app.route('/')
def hello():
    return "Flask inside Docker!!"

@app.route('/todo')
def todo():

    #_items = db.machines.find({'child'})
    query1 = {'child':{'$exists':True}}
    query2 = None
    query3 = {'type':'hardware'}
    server_list_all = query_all(None)
    items = query_all(query3)
    #items = server_list_all
    l = list(items)
    la = list(server_list_all)
    js = jsonify(l)
    return str(la)

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
def dereference_children(hware_dict):
    machines = []
    for element in hware_dict:
        hiearchy = __de_children(element)
        machines.append(hiearchy)
    return machines

def __de_children(parent):
    if 'child' in parent:
        return None
    return None
    #new_list = []
    #substitute(parent_dict)
    #for machine in parent_dict:
    #    if "child" in machine:
    #        deref = []
    #        for child in machine['child']:
    #            child_ele = query(child)
    #            deref.append(child_ele)
    #        return None
        #if "parent" in item:
        #    par_id = item["parent"]
        #    cur_id = item["_id"]

        #    return None
        #else:
        #    new_list.append(item)
    #return machine_dict

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