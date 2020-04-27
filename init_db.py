#!/usr/bin/python3
import sqlite3

def init_db(db_path):

  # connect to db and initialize cursor
  conn = sqlite3.connect(db_path)
  c = conn.cursor()

  ############################
  ########## Hours ########### 
  ############################

  # Create table
  # no rowid
  # must be unique year,month,day,hour,timestamp
  c.execute('''CREATE TABLE IF NOT EXISTS hours (
                  text text,
                  rating integer not null default 0,
                  timestamp integer not null,
                  year integer not null default 0,
                  month integer not null default 0,
                  day integer not null default 0,
                  hour integer not null default 0,
                  UNIQUE(year, month, day, hour) ON CONFLICT REPLACE
            )''')
  conn.commit()

  # Fetch data
  c.execute("SELECT rowid, * FROM hours")
  print(c.fetchall())

  ############################
  ########### Days ########### 
  ############################

  # Create table
  c.execute('''CREATE TABLE IF NOT EXISTS days (
                  text text,
                  rating integer not null default 0,
                  timestamp integer unique not null
            )''')
  conn.commit()

  # Fetch data
  c.execute("SELECT rowid, * FROM days")
  print(c.fetchall())

  ############################
  ########### Tags ########### 
  ############################

  # Create table
  c.execute('''CREATE TABLE IF NOT EXISTS tags (
                  name char(25) unique not null
            )''')

  # Insert data
  print("Inserting")
  c.execute('''INSERT INTO tags VALUES 
                  ('mytag'),
                  ('another-tag'),
                  ('last_tag')''')
  print(c.lastrowid)
  conn.commit()

  # Fetch data
  c.execute("SELECT rowid, * FROM tags")
  print(c.fetchall())

  print("Database initialized")

  conn.close()


def delete_tables(db_path):
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  c.execute('''DROP TABLE IF EXISTS hours''')
  conn.commit()
  c.execute('''DROP TABLE IF EXISTS days''')
  conn.commit()
  c.execute('''DROP TABLE IF EXISTS tags''')
  conn.commit()
  conn.close()
