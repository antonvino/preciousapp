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
      c.execute("SELECT * FROM tags")
      c.fetchall()
    except Exception as e:
      print(e)
      init_db(self.db_path)

    conn.close()


  def fetch(self, item, id = None):
    # connect to db and initialize cursor
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()

    data = []
    if id is not None:
      c.execute("SELECT * FROM {0} WHERE rowid=?".format(item), (str(id),) )
      data.append(c.fetchone())

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

    if item == "tags":
      c.execute("INSERT INTO {0} VALUES (?)".format(item), (values['name'],))
      data = {"id":c.lastrowid} # response
      conn.commit()
    
    conn.close()
    return data      
