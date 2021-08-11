# Sparkify Project (Data Lake with Apache Spark)
[![Project Passed](https://img.shields.io/badge/project-passed-success.svg)](https://img.shields.io/badge/project-passed-success.svg)

## Introduction

A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake.

## Purpose

Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

This project aims to create an ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables. This will allow their analytics team to continue finding insights in what songs their users are listening to.

## Prerequisites

##### Python3 and Python3 libraries such as below:
- configparser
- datetime
- pyspark

## Datasets

- **Song Dataset**: It consists of song name and artists on json file format.
  - **S3 Bucket**: ```s3://udacity-dend/song_data```
- **Log Dataset**: It consists of user activity for music app on json file format.
  - **S3 Bucket**: ```s3://udacity-dend/log_data```

## Structure

- **dl.cfg**: It keeps connection information for Amazon S3.
- **etl.py**: It is etl pipeline file to get data from source and store into tables.
- **README.md**: A documentation page about project.
- **test_local.ipynb**: It is a test notebook from local data source.
- **test_s3.ipynb**: It is a test notebook from Amazon S3 source.

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

- Then run "python etl.py" command to complete etl process.

- That's all :)

# THE END
