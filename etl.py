import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This function reads the song datasets and inserts them into the songs and artists tables.
    
    Pararmeters:
        cur : cursor to execute queries acquired from sparkifydb
        filepath: filepath of the JSON files to load
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    columns = df[['song_id', 'title', 'artist_id', 'year', 'duration']].columns.tolist()
    song_data = df.loc[:,columns].values[0].tolist()
    
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    art_cols = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].columns.tolist()
    artist_data = df.loc[:,art_cols].values[0].tolist()
    
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This function reads the log activity datasets and insert them into time, users, 
    and songplays tables of the sparkifydb.
    """
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    timestamp = t
    hour = t.dt.hour
    day = t.dt.day
    week = t.dt.week
    month = t.dt.month
    year = t.dt.year
    weekday = t.dt.day_name()
    
    
    time_data = ([timestamp, hour, day, week, month, year, weekday])
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'),
                         row.userId,
                         row.level,
                         songid,
                         artistid,
                         row.sessionId,
                         row.location,
                         row.userAgent
                        )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    - Get all JSON files in the specify directory
    - Process the JSON files
    - Parameter:
        cur : cursor acquired from the sparkify database (sparkifydb)
        conn : connection to postgresql and sparkify database
        filepath : the specified directory for the JSON files
        func : external function for loading the files into sparkifydb tables   
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))
        
    return all_files


def main():
    """
    This function executes all the other functions above
    Upon execution connection to the postgresql and the database sparkifydb is established 
    and cursor retrieved.
    
    It Proceeds to execute the ETL process that extract, transform and loads the songs and log 
    files into the sparkifydb tables
    
    Usage:
        execute python etl.py in the command shell
    """
    
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()