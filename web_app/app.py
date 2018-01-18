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
#server_list_all = []
#server_dict_all = {}

@app.route('/')
def hello():
    return "Flask inside Docker!!"

@app.route('/todo')
def todo():
    #init()
    #_items = db.machines.find({'child'})
    query1 = {'child':{'$exists':True}}
    query2 = None
    query3 = {'type':'hardware'}
    items = query_all(query3)
    #server_list_all = query_all(None)
    #items = server_list_all
    #l = list(items)
    list_all = dereference_children(items)
    #la = list(server_list_all)
    #js = jsonify(l)
    return str(list_all)

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
    server_dict = get_server_dict()
    machines = []
    for element in hware_dict:
        hiearchy = __de_children(element, server_dict)
        machines.append(hiearchy)
    return machines

def __de_children(parent, servers_dict):
    if 'child' in parent:
        # There can be multiple children per parent
        list_t = []
        child_list = parent['child']
        parent['child'] = [__de_children(servers_dict[x], servers_dict) for x in child_list]
    return parent

def get_server_dict():
    server_list_all = query_all(None)
    all_arr = {}
    for ele in server_list_all:
        key = ele['_id']
        value = ele
        all_arr[key] = value
    server_dict_all = all_arr
    return server_dict_all
#init(app)


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