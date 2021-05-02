# Sparkify Project (Data Modeling with Amazon Redshift)

## Introduction

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. 

## Purpose

Data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in app.

This projects aims to create ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics to continue finding insights in what songs that users are listening to. 

## Prerequisites

##### Python3 and Python3 libraries such as below:
- configparser
- psycopg2

## Datasets

- **Song Dataset**: It consists of song name and artists on json file format.
  - **S3 Bucket**: ```s3://udacity-dend/song_data```
- **Log Dataset**: It consists of user activity for music app on json file format.
  - **S3 Bucket**: ```s3://udacity-dend/log_data```

## Structure

- **dwh.cfg**: It keeps connection information for Amazon Redshift and S3.
- **create_tables.py**: It is used for create database and its tables.
- **etl.py**: It is etl pipeline file to get data from source and store into tables.
- **README.md**: A documentation page about project.
- **sql_queries.py**: It is used by etl.py to use sql queries that created for model.
- **test_queries.ipynb**: You can check data after etl process completed using this jupyter notebook.

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

- First let's open a linux terminal to run python scripts.

- Run "python create_tables.py" command at the terminal to create database and its tables.

- Finally run "python etl.py" command to complete etl process.

- That's all :)

## Useful Some Queries

1- How many users are there between 15th November and 16th November by Level?

* select level, count(distinct user_id) as user_count from songplay where start_time between '2018-11-15' and '2018-11-16' group by level

2- Find songs and artists which are on the dimension tables.

* select a.name as Artist, s.title as Song from songs s inner join artists a on s.artist_id=a.artist_id

## Some Tips

You can improve and optimize query performance by using **"DISTKEY"** and **"SORTKEY"** instead of transactional database indexes since Amazon Redshift is a columnar database with compressed storage.

# THE END