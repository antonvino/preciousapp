#!/usr/bin/python3
import sqlite3
from init_db import init_db

class PreciousData():
  """
  Class for data API
  """

  def __init__(self):
    self.db_path = "data.db"
    
    # connect to db and initialize cursor
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()

    # attempt to select from default table
    # if it fails -- create all tables for the app
    try:
      c.execute("SELECT * FROM hours")
      data = c.fetchall()
      print(data)
    except Exception as e:
      print(e)
      init_db(self.db_path)

    conn.close()


  def fetch(self, item, filters = None, one = False):
    # connect to db and initialize cursor
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()

    data = []
    if filters is not None:

      val_str = ""
      val_list = []
      for (key,val) in filters.items():
        if len(val_str) > 1:
          val_str += " AND "
        val_str += "{0}=?".format(key)
        val_list.append(val)

      c.execute("SELECT * FROM {0} WHERE {1}".format(item, val_str), tuple(val_list) )
      
      if one:
        data = c.fetchone() # single item, not list
      else:
        data = c.fetchall()

    else:
      c.execute("SELECT * FROM {0}".format(item))
      data = c.fetchall()
    
    conn.close()
    return data      


  def delete_all(self, item):
    # connect to db and initialize cursor
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()

    c.execute("DELETE FROM {0}".format(item))
    conn.commit()


  def insert_many(self, item, values):
    # connect to db and initialize cursor
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    data = []

    val_str = ""
    for (i,val) in enumerate(values):
      if i > 0:
        val_str += ", "
      val_str += "(?)"

    if item == "tags":
      val_list = []
      for (i,val) in enumerate(values):
        val_list.append(val['name'])
      
      c.execute("INSERT INTO {0} VALUES {1}".format(item, val_str), tuple(val_list))
      data = {"id":c.lastrowid} # response
      conn.commit()
    
    conn.close()
    return data      


  def insert(self, item, values):
    # connect to db and initialize cursor
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    data = []

    val_str = ""
    val_list = []
    for (i,val) in enumerate(values):
      if i > 0:
        val_str += ", "
      val_str += "?"
      val_list.append(val)

    if item == "hours":

      print(val_str)
      print(val_list)
      c.execute("INSERT INTO {0} VALUES ({1})".format(item, val_str), tuple(val_list))
      data = {"id":c.lastrowid} # response
      conn.commit()
    
    conn.close()
    return data      
