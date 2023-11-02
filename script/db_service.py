import json
import uuid
from datetime import datetime
from pytz import UTC

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
        print(f"Data - {data_dict}")
        pmitemmasterform_id = str(pmitemmasterform_id)
        
        current_time = datetime.now(UTC)
        created_at = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')


        
        insert_query = '''
        INSERT INTO "{}" ("pmitemmasterform_id", "company_id", "form_json", "asset_class_code", "asset_class_name", "plan_name", "pm_title", "created_at")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        '''.format(table_name)

        cur.execute(insert_query, (
            pmitemmasterform_id,
            data_dict['company_id'],
            data_dict['form_json'],
            data_dict['asset_class_code'],
            data_dict['asset_class_name'],
            data_dict['plan_name'],
            data_dict['pm_title'],
            created_at
        ))
        print(f"data inserted for UUID >> {pmitemmasterform_id}")
        conn.commit()  

    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()  
        print("***** \n Exception in addrecordsdb:", error)
        return None, 0
    finally:
        cur.close()
        conn.close()
        print('Database connection closed.')

