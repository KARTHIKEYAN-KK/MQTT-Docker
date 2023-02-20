from flask import Flask, request

app = Flask(__name__)

stores =[
    {
        "name":"Storeone",
        "items":[
            {
                "name":"item1",
                "price":100
            },
            {
                "name":"item2",
                "price":150
            }
        ]
    }
]

@app.get("/store")
def get_store():
    return{"Stores":stores}

@app.get("/store/<string:name>")
def get_indistore(name):
    for store in stores:
        if store["name"] == name:
            return store
    return{"message":"Store not found"}, 404

@app.get("/store/<string:name>/items")
def get_items(name):
    for store in stores:
        if store["name"] == name:
            return {"items":store["items"]}


@app.post("/store")
def add_store():
    req_data = request.get_json()
    new_store = {"name":req_data["name"], "items":[]}
    stores.append(new_store)
    return new_store, 201

@app.post("/store/<string:name>/items")
def add_items(name):
    req_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name":req_data["name"], "price":req_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return{"message":"Store not found"}, 404
