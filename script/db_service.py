import json
import uuid
from datetime import datetime

import psycopg2
from config import config

def db_connection():
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        return conn, cur

    except (Exception, psycopg2.DatabaseError) as error:
        print("***** \n Exception in db connection method: ", error)
        return 0,0



def addrecordsdb(table_name, data_dict):
    conn, cur = db_connection() 

    try:
        
        pmitemmasterform_id = uuid.uuid4()
#         pmitemmasterform_id = str()
        print(pmitemmasterform_id)
        print(type(pmitemmasterform_id))
        
        pmitemmasterform_id = str(pmitemmasterform_id)
        
        print(pmitemmasterform_id)
        print(type(pmitemmasterform_id))
        
        insert_query = '''
        INSERT INTO "{}" ("pmitemmasterform_id", "company_id", "form_json", "asset_class_code", "asset_class_name", "plan_name", "pm_title")
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        '''.format(table_name)

        cur.execute(insert_query, (
            pmitemmasterform_id,
            data_dict['company_id'],
            data_dict['form_json'],
            data_dict['asset_class_code'],
            data_dict['asset_class_name'],
            data_dict['plan_name'],
            data_dict['pm_title']
        ))

        conn.commit()  

    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()  
        print("***** \n Exception in addrecordsdb:", error)
        return None, 0
    finally:
        cur.close()
        conn.close()
        print('Database connection closed.')

