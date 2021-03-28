# Sparkify Project (Data Modeling with Postgres)

## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Purpose

This projects aims to create a data model on Postgres and build ETL pipeline using Python.

## Prerequisites

##### Python3 and Python3 libraries such as below:
- os
- glob
- psycopg2
- pandas

## Datasets

- **Song Data**: It consists of song name and artists on json file format.
- **Log Data**: It consists of user activity for music app on json file format.

## Structure

- **data**: It is a directotry that keeps data which is about song and log (user activity) on json file format.
- **create_tables.py**: It is used for create database and its tables.
- **etl.ipynb**: It is jupyter notebook to test development process before implement etl.py
- **etl.py**: It is etl pipeline file to get data from source and store into tables.
- **README.md**: A Documentation page about project.
- **sql_queries.py**: It is used by etl.py to use sql queries that created for model.
- **test.ipynb**: You can check data after etl process completed using this jupyter notebook.

## Schema

### Fact Tables

**songplays:** records in log data associated with song plays

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

## Some Statiscs About Data

* Song Data: 71 Files
* Log Data: 30 Files
* Fact Table: 6820 Rows
* Number of Users: 96
* Number of Songs: 71
* Number of Artists: 69

## Useful Some Queries

1- How many users are there between 15th November and 16th November by Level?

* select level, count(distinct user_id) as user_count from songplays where start_time between '2018-11-15' and '2018-11-16' group by level

2- Find songs and artists which are on the dimension tables.

* select a.name as Artist, s.title as Song from songs s inner join artists a on s.artist_id=a.artist_id

## Last Note

There is only one matching row with log data and dimension tables after etl process such as below:
* song_id = SOZCTXZ12AB0182364
* artist_id = AR5KOSW1187FB35FF4

# THE END
