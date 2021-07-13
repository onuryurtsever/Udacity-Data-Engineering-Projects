from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 table = "",
                 sql = "",
                 truncate = False,
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql
        self.truncate = truncate

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if not self.truncate:
            redshift.run("TRUNCATE TABLE {}".format(self.table))
        
        insert_fact = f"INSERT INTO {self.table} {self.sql};"
        redshift.run(insert_fact)
        
        self.log.info(f"Job is Successful: Inserting to {self.table} from staging tables")
