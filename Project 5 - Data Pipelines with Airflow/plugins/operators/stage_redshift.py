from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    
    template_fields = ("s3_key",)
    
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        REGION AS '{}'
        FORMAT AS JSON '{}'
        TIMEFORMAT as 'epochmillisecs'
        TRUNCATECOLUMNS
        BLANKSASNULL
        EMPTYASNULL
        COMPUPDATE OFF
        ;
    """

    @apply_defaults
    def __init__(self,
                 table="",
                 redshift_conn_id="",
                 aws_credentials_id="",
                 s3_bucket="",
                 s3_key="",
                 region="us-west-2",
                 json_format="",
                 extra_params="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.region = region
        self.json_format = json_format
        self.extra_params = extra_params

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        redshift.run("TRUNCATE TABLE {}".format(self.table))
        
        s3_path = "s3://{}/{}/".format(self.s3_bucket, self.s3_key)
        
        copy_statement = StageToRedshiftOperator.copy_sql.format(
         self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.region,
            self.json_format
        )
        
        redshift.run(copy_statement)
        self.log.info(f"Job is Successful: Copying {self.table} from S3 to Redshift")





