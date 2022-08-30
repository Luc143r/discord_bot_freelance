from pymongo import MongoClient
from config import settings_db


client = MongoClient(settings_db['host_db'], settings_db['port_db'])
db = client[settings_db['name_db']]
collection = db[settings_db['collection_db']]


def get_data(collection, elements, multiple=False):
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


"""data_ds = {
    'wallet': 'EQD7y8d1ImET4WqHclpIJVED2WHKCXb4U3riNV6spyWmzuya',
    'username_ds': '',
    'username_tg': '@insearchofmyself666',
    'points': 0,
}"""

def update_data(collection, query_elements, new_values):
    collection.update_one(query_elements, {'$set': new_values})

def insert_data(collection, data):
    if not get_data(collection, {'wallet': data['wallet']}):
        print('User add')
        return collection.insert_one(data).inserted_id
    else:
        if not get_data(collection, {'wallet': data['wallet']})['username_ds']:
            wallet = get_data(collection, {'wallet': data['wallet']})['wallet']
            update_data(collection, {'wallet': wallet}, {'username_ds': data['username_ds']})
            print('Username_ds add')
        else:
            print('Username_ds found')

#insert_data(collection, data_ds)
