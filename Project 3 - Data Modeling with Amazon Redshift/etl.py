import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    This function calls to insert data 
    from S3 into stage tables on AWS Redshift.
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    This function is used to fill
    fact and dimension tables on AWS Redshift.
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    This is main function that use functions such as load_staging tables and insert_tables.
    Code runs first main function and use these functions above.
    """ 
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()