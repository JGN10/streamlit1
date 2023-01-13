import setting
import psycopg2
import pymongo

def connect_postgre():
    print('dentro de connect')
    conn = psycopg2.connect(database=setting.DATABASE,
                            user=setting.USER,
                            password=setting.PASSWORD,
                            host=setting.HOST,
                            port=setting.PORT)

    cur = conn.cursor()
    return cur, conn

def connect_mongo(nombredb):

    # # conexión a base de datos
    bbdd = pymongo.MongoClient(setting.HOST_MONGO, setting.PORT_MONGO)

    # # Si no existe la base de datos la crea con el nombre qye haya en nombredb
    db = bbdd[nombredb]

    return db