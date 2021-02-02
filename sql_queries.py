# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS fact_songplay"
user_table_drop = "DROP TABLE IF EXISTS dim_user"
song_table_drop = "DROP TABLE IF EXISTS dim_song"
artist_table_drop = "DROP TABLE IF EXISTS dim_artist"
time_table_drop = "DROP TABLE IF EXISTS dim_time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS fact_songplay (
    songplay_id int, start_time time, user_id int, level varchar, song_id, artist_id, session_id, location, user_agent
    )
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS dim_user (
    user_id int, first_name varchar, last_name varchar, gender varchar, level varchar
    )
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS dim_song (
    song_id int, title varchar, artist_id, year int, duration numeric(18,5)
    )
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS dim_artist (
    artist_id int, name varchar, location varchar, latitude numeric(10,6), longitude numeric(10,6)
    )
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS dim_time (
    start_time, hour, day, week, month, year, weekday
    )
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]