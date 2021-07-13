from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tables=[],
                 sql_query="",
                 failure_value="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables
        self.sql_query = sql_query
        self.failure_value = failure_value
        
    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        for table in self.tables:
            
            number_of_records = redshift.get_records(f"SELECT COUNT(*) FROM {table}")
        
            sql_query = self.sql_query.format(table)
            result = redshift.get_first(sql_query)[0]
        
            if result == self.failure_value :
                raise ValueError(f"Data quality check is failed on query {sql_query}, failure {self.failure_value}")
        
            self.log.info(f"Data quality check is passed on {table} table that contains {number_of_records[0][0]} rows.")