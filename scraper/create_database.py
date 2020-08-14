# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 17:26:01 2020

@author: ali_e

Creating database using sqlite to store scraped player data.

References:
    https://www.sqlitetutorial.net/sqlite-python/creating-database/
"""

import sqlite3
from sqlite3 import Error
import os


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    
    #get root project directory
    ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
    #get data directory
    DATA_DIR = os.path.join(ROOT_DIR, 'data')
    #Assigning database file which will be located in data directory
    database = os.path.join(DATA_DIR, 'warzone.db')

    sql_create_players_table = """ CREATE TABLE IF NOT EXISTS players (
                                        id integer PRIMARY KEY,
                                        player_name text NOT NULL,
                                        platform text NOT NULL,
                                        scrape_id integer NOT NULL,
                                        FOREIGN KEY (scrape_id) REFERENCES scrape_log (session_id)
                                    ); """

    sql_create_stats_table = """CREATE TABLE IF NOT EXISTS stats (
                                    id integer PRIMARY KEY,
                                    player_id integer NOT NULL,
                                    matches_played integer,
                                    time_played text,
                                    wins integer,
                                    top_5 integer,
                                    top_10 integer,
                                    top_25 integer,
                                    kills integer,
                                    deaths integer,
                                    kd_ratio real,
                                    downs integer,
                                    avg_life text,
                                    score_per_game real,
                                    score_per_min real,
                                    contracts integer,
                                    scrape_id integer NOT NULL,
                                    FOREIGN KEY (scrape_id) REFERENCES scrape_log (session_id), 
                                    FOREIGN KEY (player_id) REFERENCES players (id)
                                );"""

    sql_create_weeklystats_table = """ CREATE TABLE IF NOT EXISTS weekly_stats (
                                        id integer PRIMARY KEY,
                                        player_id integer NOT NULL,
                                        scrape_id integer NOT NULL,
                                        game_type text NOT NULL,    /* eg. BR quads */
                                        matches_played integer,
                                        kd_ratio real,
                                        kills_per_game real,
                                        headshot_pct real,
                                        score_per_min real,
                                        score_per_game real,
                                        damage_per_min real,
                                        damage_per_game real,
                                        avg_life text,
                                        team_wiped integer,
                                        last_stand_kills integer,
                                        caches integer,  /* starting here, switch to matches page */
                                        wins integer,
                                        top_5 integer,
                                        top_10 integer,
                                        top_25 integer,
                                        win_avg_kills real,
                                        win_avg_caches real,
                                        win_avg_damage real,
                                        win_avg_damage_per_min real,
                                        FOREIGN KEY (scrape_id) REFERENCES scrape_log (session_id),
                                        FOREIGN KEY (player_id) REFERENCES players (id)
                                    ); """
    
    #need to determine what needs to be logged for each scraping session
    sql_create_scrapelog_table = """ CREATE TABLE IF NOT EXISTS scrape_log (
                                        session_id integer PRIMARY KEY,
                                        start_date text NOT NULL,
                                        end_date text NOT NULL,
                                        num_players int NOT NULL,
                                        num_pages int NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create players table
        create_table(conn, sql_create_players_table)

        # create stats table
        create_table(conn, sql_create_stats_table)
        
        #create weekly_stats table
        create_table(conn, sql_create_weeklystats_table)
        
        #create scrape_log table
        create_table(conn, sql_create_scrapelog_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()