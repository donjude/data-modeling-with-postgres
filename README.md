# Data modeling with Postgres - Sparkify ETL and Pipeline

## Context

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

Your role as a Data Engineer is to designed and create an Optimized Postgres database schema and ETL pipeline for this analysis.

### Datasets

There are two different datasets format:
- **Song datasets:** Each file is in JSON format and contains metadata about a song and the artist of that song.

```json
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

- **Log datasets:** The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app are based on specified configurations.

    **sample**

```json
{"artist":null,"auth":"Logged In","firstName":"Walter","gender":"M","itemInSession":0,"lastName":"Frye","length":null,"level":"free","location":"San Francisco-Oakland-Hayward, CA","method":"GET","page":"Home","registration":1540919166796.0,"sessionId":38,"song":null,"status":200,"ts":1541105830796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"39"}
```

## Database Schema
The star schema was used in the database modeling of this project. The star schema consists of one fact table which contains all the measurable and quantitative data about each song. It references 4 different dimension tables that consists of descriptive attributes related to the fact table.

### Fact Table
This contains the measurable and quantitative data about each song. Below is the single fact table and its SQL code.

- **songplays** - records in log data associated with song plays i.e. records with page NextSong.
    - *songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*
    
    ```sql
    CREATE TABLE IF NOT EXISTS songplays
    (
        songplay_id SERIAL PRIMARY KEY 
        ,start_time TIMESTAMP REFERENCES time(start_time)
        ,user_id int NOT NULL REFERENCES users(user_id)
        ,level text
        ,song_id text REFERENCES songs(song_id)
        ,artist_id text REFERENCES artists(artist_id)
        ,session_id int
        ,location text
        ,user_agent text
    )
    ```
    
### Dimension Tables
These tables references the fact table and contains descriptive attributes related to the fact table. Below are all the 4 tables and their sql codes.

- **users** - users in the app
    - *user_id, first_name, last_name, gender, level*
    
    ```sql
    CREATE TABLE IF NOT EXISTS users
    (
        user_id int PRIMARY KEY
        ,first_name text NOT NULL 
        ,last_name text NOT NULL
        ,gender text
        ,level text
    )
    ```


- **songs** - songs in music database
    - *song_id, title, artist_id, year, duration*
    
    ```sql
    CREATE TABLE IF NOT EXISTS songs
    (
        song_id text PRIMARY KEY
        ,title text NOT NULL
        ,artist_id text NOT NULL
        ,year int
        ,duration float NOT NULL
    )
    ```


- **artists** - artists in music database
    - *artist_id, name, location, latitude, longitude*
    
    ```sql
    CREATE TABLE IF NOT EXISTS artists
    (
        artist_id text PRIMARY KEY
        ,name text NOT NULL
        ,location text 
        ,lattitude float 
        ,longitude float
    )
    ```


- **time** - timestamps of records in songplays broken down into specific units
    - *start_time, hour, day, week, month, year, weekday*
    
    ```sql
    CREATE TABLE IF NOT EXISTS time
    (
        start_time TIMESTAMP PRIMARY KEY
        ,hour int
        ,day int
        ,week int
        ,month int
        ,year int
        ,weekday text
    )
    ```

## Project Setup
The project setup consist of the data and all the scripts require to reproduce this project.

- `data` - This folder contains all the relevant JSON files for both songs and log files.
- `sql_queries.py` - This script contains all the SQL queries for creating all the tables and inserting data into the tables.
- `create_tables.py` - This script contains code for dropping and creating a database. It executes the create and drop tables queries in `sql_queries.py`
- `etl.ipynb` - This notebook if for the initial coding and testing of the etl process.
- `etl.py` - This script implements the codes in the `etl.ipynb` notebook for a smooth extract transform and loading of the datasets into the database.
- `test.ipynb` - This notebook test to see if data was inserted successfully into the database tables.

### Run Script
To run the script:
1. Execute `python create_tables.py` in the command console or jupyterlab terminal to drop, create database and tables in sparkifydb.
2. Execute `python etl.py` in the command console or jupyterlab terminal to extract the source files, transform the files and load them into the various fact and dimension tables.
3. Run the script in the notebook `test.ipynb` to test if the etl process loaded the files successfully.