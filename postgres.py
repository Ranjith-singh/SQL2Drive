import sys
import psycopg2
import os
import constants

def init():
    print("initializing database...")
    configs = constants.configs
    with open(str(os.getcwd())+'/.config', 'rb') as read_prop:
        configs.load(read_prop)
        
    try:
        conn = psycopg2.connect(
                database=configs.get("db_name").data,
                user=configs.get("db_user").data,
                host=configs.get("db_host").data, 
                password=configs.get("db_password").data,
                port=configs.get("db_port").data
            )
        print("Connected!!!")
        constants.DATABASE_CONNECTIONS['db'] = conn
        
    except Exception as e:
        sys.exit(f"Connection not happened: {e}")
        
def close_connection():
    try:
        for conn in constants.DATABASE_CONNECTIONS:
            constants.DATABASE_CONNECTIONS[conn].close()
        print(f'connections closed')
    except Exception as e:
        print(f'connection closing error {e}') 
        