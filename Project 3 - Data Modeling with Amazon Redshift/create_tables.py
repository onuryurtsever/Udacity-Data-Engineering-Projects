import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    This function drops whole tables 
    in the Amazon Redshift database 
    which is modelled in sql_queries.py file."
    """ 
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    This function create whole tables 
    in the Amazon Redshift database 
    which is modelled in sql_queries.py file."
    """ 
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    This is the main function which code runs first at this section.
    It calls drop_tables and create_tables functions to complete process.
    """ 
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()