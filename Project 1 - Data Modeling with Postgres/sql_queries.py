# DROP TABLES

songplay_table_drop = "drop table if exists songplays;"
user_table_drop = "drop table if exists users;"
song_table_drop = "drop table if exists songs;"
artist_table_drop = "drop table if exists artists;"
time_table_drop = "drop table if exists time;"

# CREATE TABLES

songplay_table_create = ("""
create table if not exists songplays (
songplay_id serial, 
start_time timestamp NOT NULL, 
user_id int NOT NULL, 
level varchar NOT NULL, 
song_id varchar NULL, 
artist_id varchar NULL, 
session_id int NOT NULL, 
location varchar NOT NULL, 
user_agent varchar NOT NULL,
primary key (songplay_id)
);
""")

user_table_create = ("""
create table if not exists users (
user_id int NOT NULL, 
first_name varchar NOT NULL, 
last_name varchar NOT NULL, 
gender varchar NOT NULL, 
level varchar NOT NULL,
primary key (user_id)
);
""")

song_table_create = ("""
create table if not exists songs (
song_id varchar, 
title varchar NOT NULL, 
artist_id varchar NOT NULL, 
year int NOT NULL, 
duration float NOT NULL,
primary key (song_id)
);
""")

artist_table_create = ("""
create table if not exists artists (
artist_id varchar, 
name varchar NOT NULL, 
location varchar NULL, 
latitude float NULL,
longitude float NULL,
primary key (artist_id)
);
""")

time_table_create = ("""
create table if not exists time (
start_time timestamp NOT NULL, 
hour int NOT NULL, 
day int NOT NULL, 
week int NOT NULL, 
month int NOT NULL, 
year int NOT NULL, 
weekday int NOT NULL,
primary key (start_time)
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
insert into songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
values (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")

user_table_insert = ("""
insert into users (user_id, first_name, last_name, gender, level)
values (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level
""")

song_table_insert = ("""
insert into songs (song_id, title, artist_id, year, duration)
values (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""
insert into artists (artist_id, name, location, latitude, longitude) 
values (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")

time_table_insert = ("""
insert into time (start_time, hour, day, week, month, year, weekday)
values (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")

# FIND SONGS

song_select = ("""select s.song_id,s.artist_id from songs s inner join artists a on s.artist_id=a.artist_id where s.title=(%s) and a.name=(%s) and s.duration=(%s);""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]