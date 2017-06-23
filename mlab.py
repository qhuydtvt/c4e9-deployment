import mongoengine

#mongodb://<dbuser>:<dbpassword>@ds127872.mlab.com:27872/lingeries_shop

host = "ds127872.mlab.com"
port = 27872
db_name = "lingeries_shop"
user_name = "admin"
password = "admin"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())