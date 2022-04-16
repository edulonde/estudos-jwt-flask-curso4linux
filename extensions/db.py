from os import getenv
import pymongo


def get_conn(database):
    client = None

    try:
        client = pymongo.MongoClient(getenv("MONGO_URI"))
    except Exception as e:
        return {
            'ACK': False,
            'message': f'não foi possível conectar ao banco de dados: {e}'
        }
    return client.get_database(database)
