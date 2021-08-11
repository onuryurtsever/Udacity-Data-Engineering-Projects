# Data Engineering Capstone Project
[![Project Passed](https://img.shields.io/badge/project-passed-success.svg)](https://img.shields.io/badge/project-passed-success.svg)

# Data Lake for U.S. Immigration Office

## Project Summary
In this project we are creating data lake about U.S. Immigrants and their behaviours which are related to city, temperature, airport.

The project follows the follow steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up

## Purpose

We aim to ask some questions such as below:

* Why immigrants do choose these cities?
* Do they like mostly hot or warmer cities?
* Demographic structure is reason to choose these cities?

Therefore U.S. Immigrant Office will be able to take better decisions in their policies.

## Prerequisites

##### Python3 and Python3 libraries such as below:
- pandas
- pyspark

## Datasets

- **I94 Immigration Data**
- **World Temperature Data**
- **U.S. City Demographic Data**
- **Airport Code Table**

## Schema

Star Schema is the selected model which is easy and effective to create queries by joining fact and dimension tables for analysing data.

##### Stage Tables

* stg_temperature
* stg_demoghraphy
* stg_airport
* stg_immigration

##### Dimension Tables

* dim_temperature
* dim_demography
* dim_airport
* dim_time

##### Fact Tables

* fct_immigration

#### 4.4 Some Queries and Analysing Data
##### Let's query on data for our questions

First we will read our fact and dimension tables under directory which is "fact_dimension", in parquet format.

- **dim_temperature:** It consists of only U.S. cities. Here we wil use "City" column to join other datasets.
- **dim_demography:** It consists of only demographic structure of U.S. cities. "City" and "State" colums will be used for joining other datasets.
- **dim_airport:** It consists of only U.S. airports that are small, medium, large airports. Here "municipality" column will be joined over "City" columns with other datasets.
- **dim_time:** It is time dimension tables which is created by immigrant datasets. Here we used "arrival_date" to create time dimension table.

I will try join datasets with city or state columns. So let's see what happens.

First let's check city temperature - number of arrivals relationship.

I will accept 18 celcius degree as threshold. It means If city is higher than or equal 18, it is warm place else it is cold.
So I will assign a flag for this cities in query.

![IMMIGRATION](https://raw.githubusercontent.com/onuryurtsever/Udacity-Data-Engineering-Projects/main/Project%206%20-%20Capstone%20Project/images/immigration.PNG)

According to results, ratios are nearly so close. So we can't say definitely immigrants choose cities because of climate.

#### Some Notes

* As you see in the project, Spark is used for extracting, transforming and load operations since it has large data processing in memory compute. Also we can use Spark in cloud environment such as AWS EMR that have distributed nodes, processing data fast.

* If we had production environment, architecture would be like this below:

**AWS S3 --> AWS EMR (Spark Jobs) --> Apache Airflow --> AWS Redshift**

* According to data analysis of i94, monthly update is enough and we can schedule it via Apache Airflow in production environment.

 * **The data was increased by 100x:**
 We deploy our Spark solution to AWS EMR to compute more fast. Also cloud enviroment will scale itself if data becomes larger.
 
 * **The data populates a dashboard that must be updated on a daily basis by 7am every day:**
 We can use Apache Airflow to schedule and manage our data pipelines in production environment.
 
 * **The database needed to be accessed by 100+ people:**
 Our fact and dimension tables are in parquet format. So we can copy them to HDFS or AWS S3 and show them as external table by using Apache Hive. So people can connect Hive via their dashboard tools.

# THE END
