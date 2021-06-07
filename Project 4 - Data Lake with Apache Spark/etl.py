import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, monotonically_increasing_id
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['AWS_SECRET_ACCESS_KEY']
os.environ['AWS_REGION']=config['AWS']['AWS_REGION']

def create_spark_session():
    """
    This function is used to 
    create Spark session in server
    to run PySpark applications.
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark

def process_song_data(spark, input_data, output_data):
    """
    This function gets input_data from any source
    such as S3, HDFS and saves data into parquet files
    as output on any destionation
    after creating dimensional tables from json files.
    """
    # get filepath to song data file
    song_data = input_data + "song_data/*/*/*/*.json"
    
    # read song data file
    print("Reading song_data is started...")
    df = spark.read.json(song_data)
    print("Reading song_data is completed.")

    # extract columns to create songs table
    df.createOrReplaceTempView("songs")
    songs_table = spark.sql("select distinct song_id, title, artist_id, year, duration from songs")
    
    # write songs table to parquet files partitioned by year and artist
    print("Writing songs.parquet is started...")
    songs_table.write.partitionBy("year", "artist_id").parquet(path = output_data + "songs.parquet", mode = "overwrite")
    print("Writing songs.parquet is completed.")

    # extract columns to create artists table
    df.createOrReplaceTempView("artists")
    artists_table = spark.sql("""select distinct artist_id, 
                            artist_name as name, 
                            artist_location as location, 
                            artist_latitude as latitude, 
                            artist_longitude as longitude 
                            from artists
                          """) 
    
    # write artists table to parquet files
    print("Writing artists.parquet is started...")
    artists_table.write.parquet(path = output_data + "artists.parquet", mode = "overwrite")
    print("Writing artists.parquet is completed.")

def process_log_data(spark, input_data, output_data):
    """
    This function gets input_data from any source
    such as S3, HDFS and saves data into parquet files
    as output on any destionation
    after creating dimensional and fact tables 
    by joining song and event logs from json files.
    """
    # get filepath to log data file
    log_data = input_data + "log_data/*/*/*.json"

    # read log data file
    print("Reading log_data is started...")
    df = spark.read.json(log_data)
    print("Reading log_data is completed.")
    
    # filter by actions for song plays
    df.createOrReplaceTempView("stg_events")
    songplays_table = spark.sql("select * from stg_events where page='NextSong'")

    # extract columns for users table    
    df.createOrReplaceTempView("users")
    users_table = spark.sql("select distinct userId, firstName, lastName, gender, level from users")
    
    # write users table to parquet files
    print("Writing users.parquet is started.")
    users_table.write.parquet(path = output_data + "users.parquet", mode = "overwrite")
    print("Writing users.parquet is completed.")

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: str(int(int(x)/1000)))
    df = df.withColumn('time_stamp', get_timestamp(df.ts))
    
    # create datetime column from original timestamp column
    get_timestamp = udf(lambda x: str(datetime.fromtimestamp(int(x) / 1000.0)))
    df = df.withColumn("start_time", get_timestamp("ts"))
    
    # extract columns to create time table
    df.createOrReplaceTempView("time")
    time_table = spark.sql("""select distinct time_stamp as start_time, 
                                        hour(start_time) as hour, 
                                        day(start_time) as day, 
                                        weekofyear(start_time) as week, 
                                        month(start_time) as month, 
                                        year(start_time) as year, 
                                        dayofweek(start_time) as weekday 
                           from time
                       """)
    
    # write time table to parquet files partitioned by year and month
    print("Writing time.parquet is started...")
    time_table.write.partitionBy("year", "month").parquet(path = output_data + "time.parquet", mode = "overwrite")
    print("Writing time.parquet is completed.")

    # read in song data to use for songplays table
    print("Reading songs.parquet is started...")
    song_df = spark.read.parquet(output_data + "songs.parquet")
    print("Reading songs.parquet is completed.")
    
    song_df.createOrReplaceTempView("stg_songs")

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = spark.sql("""select
                    events.ts start_time,
                    events.userId user_id,
                    events.level,
                    songs.song_id,
                    songs.artist_id,
                    events.sessionId session_id,
                    events.location,
                    events.userAgent user_agent
                    from stg_events events inner join stg_songs songs
                    on events.song=songs.title
                    where events.page='NextSong'
"""
)
    songplays_table = songplays_table.withColumn("songplay_id", monotonically_increasing_id())
    
    songplays_joined_time = songplays_table.join(time_table, (songplays_table.start_time == time_table.start_time), how="inner") \
    .select("songplay_id", songplays_table.start_time, "user_id", "level", "song_id", "artist_id", "session_id", "location", "user_agent", "year", "month")

    # write songplays table to parquet files partitioned by year and month
    print("Writing songplays.parquet is started...")
    songplays_joined_time.write.partitionBy("year", "month").parquet(path = output_data + "songplays.parquet", mode = "overwrite")
    print("Writing songplays.parquet is completed.")

def main():
    """
    This is the main section of python code to run application.
    Application starts first here and calls necessary functions
    to move on process.
    """
    print("Spark Session is being created...")
    spark = create_spark_session()
    print("Spark Session is created.")
    
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-store/"
    
    start = datetime.now()
    print("Job started.")
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)
    
    end = datetime.now()    
    duration = end - start    
    print("Job finished in {}.".format(duration))
    
if __name__ == "__main__":
    main()
