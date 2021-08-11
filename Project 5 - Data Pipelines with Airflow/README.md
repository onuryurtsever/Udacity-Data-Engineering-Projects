# Sparkify Project (Data Pipelines with Airflow)

## Introduction

A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

## Purpose

They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Prerequisites

- Apache Airflow
- Python 3
- AWS S3
- AWS Redshift

## Datasets

- **Song Dataset**: It consists of song name and artists on json file format.
  - **S3 Bucket**: ```s3://udacity-dend/song_data```
- **Log Dataset**: It consists of user activity for music app on json file format.
  - **S3 Bucket**: ```s3://udacity-dend/log_data```

## Pipeline Diagram



## Structıre

- **udac_example_dag.py:** Main DAG file which contains configuration and pipeline structure.
- **sql_queries.py:** It contains sql queries which is used in ETL process.
- **stage_redshift.py:** It reads data from AWS S3 and stores them into stage tables in AWS Redshift database.
- **data_quality.py:** It validates date that is in AWS Redshift database.
- **load_dimension.py:** It loads into dimension tables from stages tables.
- **load_fact.py:** It loads into fact table from stage tables.

## Schema

### Fact Tables

**songplay:** records in log data associated with song plays

**columns:** songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables

1- **users:** users in the app

**columns:** user_id, first_name, last_name, gender, level

2- **songs:** songs in music database

**columns:** song_id, title, artist_id, year, duration

3- **artists:** artists in music database

**columns:** artist_id, name, location, latitude, longitude

4- **time:** timestamps of records in songplays broken down into specific units

**columns:** start_time, hour, day, week, month, year, weekday

## How to Use

After you have updated the DAG, you will need to run /opt/airflow/start.sh command to start the Airflow web server. Once the Airflow web server is ready, you can access the Airflow UI.

# THE END