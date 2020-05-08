#!/usr/bin/python3
import time
from datetime import datetime, timedelta, date
from data import PreciousData

class PreciousApp:
  """
  Class for generic application functions
  """

  def __init__(self):
    self.load_current_time()
    self.data = PreciousData()


  def load_current_time(self):
    """
    Takes current timestamp and updates the date/time data
    """
    self.curr_timestamp = time.time()
    self.curr_time = datetime.fromtimestamp(self.curr_timestamp)     
    self.year = self.curr_time.year
    self.month = self.curr_time.month
    self.day = self.curr_time.day
    self.hour = int(self.curr_time.strftime('%H')) # need a 24 hour


  def load_time(self, timestamp):
    """
    Takes given timestamp and updates the date/time data
    """
    self.curr_timestamp = timestamp
    self.curr_time = datetime.fromtimestamp(self.curr_timestamp)     
    self.year = self.curr_time.year
    self.month = self.curr_time.month
    self.day = self.curr_time.day
    self.hour = int(self.curr_time.strftime('%H')) # need a 24 hour   


  def get_time(self, timestamp):
    """
    Takes given timestamp and gets the date/time data
    """
    curr_time = datetime.fromtimestamp(timestamp)
    return {
      "time": curr_time,
      "hour": int(self.curr_time.strftime('%H')) # need a 24 hour   
    }


  def get_hour_short_label(self, label_time = None):
    if label_time is not None:
      return label_time.strftime('%I %p')
    else:
      return self.curr_time.strftime('%I %p')


  def get_hour_label(self, label_time = None):
    if label_time is not None:
      return label_time.strftime('%a %d %b, %I %p')
    else:
      return self.curr_time.strftime('%a %d %b, %I %p')
    # self.day_label = label_time.strftime('%a %d %b')
    # self.day_button = label_time.strftime('%a %d %b')

    # if self.activity:
    #   self.hourField.setStringValue_(self.activity)
    #   self.hourLabel.setTextColor_(NSColor.blackColor())
    # else:
    #   self.hourField.setStringValue_('')
    #   # if not self.productive and self.productive != 0:
    #   self.hourLabel.setTextColor_(NSColor.redColor())
    # if self.productive or self.productive == 0:
    #   self.hourSegment.setSelected_forSegment_(1, self.productive)
    # else:
    #   self.hourSegment.setSelected_forSegment_(1, 1)

  def get_hour_text(self):
    if 'text' in self.hour_data:
      return self.hour_data['text']
    else:
      return 'Log hour'


  def to_prev_hour(self):
    self.load_time(self.curr_timestamp - 3600)


  def to_next_hour(self):
    self.load_time(self.curr_timestamp + 3600)


  def change_hour(self, change):
    self.load_time(self.curr_timestamp + 3600 * change)


  def load_hour(self):
    filters = {
      "year": self.year,
      "month": self.month,
      "day": self.day,
      "hour": self.hour
    }
    data = self.data.fetch("hours", filters, True)
    if data is None:
      self.hour_data = {
        "id": 0,
        "text": "",
        "rating": 0,
        "timestamp": int(self.curr_timestamp),
        "year": self.year,
        "month": self.month,
        "day": self.day,
        "hour": self.hour
      }
    else:
      self.hour_data = {
        "id": data[0],
        "text": data[1],
        "rating": data[2],
        "timestamp": data[3],
        "year": data[4],
        "month": data[5],
        "day": data[6],
        "hour": data[7]
      }

  def get_tags(self, decorator = ""):
    tags = []
    data = self.data.fetch("tags")
    for tag in data:
      tags.append("{0}{1}".format(decorator, tag[1]))
    # return the tags list
    return tags

  def get_item_tags(self, item = None, id = None, decorator = ""):
    tags = []
    data = self.data.get_tags(item, id)
    for tag in data:
      tags.append("{0}{1}".format(decorator, tag[1]))
    # return the tags list
    return tags


  def save_tags(self, tags):
    self.data.delete_all("tags")
    self.add_tags(tags)


  def add_tags(self, tags):
    db_tags = []
    for tag in tags:
      db_tags.append({"name": tag})
    self.data.insert_many("tags",db_tags)


  def save_hour(self, text, rating, selected_tags):
    self.hour_data['text'] = text
    self.hour_data['rating'] = rating
    self.hour_data['timestamp'] = int(self.curr_timestamp)
    self.hour_data['year'] = self.year
    self.hour_data['month'] = self.month
    self.hour_data['day'] = self.day
    self.hour_data['hour'] = self.hour

    db_hour = [text, rating, int(self.curr_timestamp), self.year, self.month, self.day, self.hour]
    new_hour = self.data.insert("hours", db_hour)
    self.hour_data['id'] = new_hour['id']

    # delete all attached tags that could exist for this hour
    self.data.delete_all("tags_hours", {"hour_id": new_hour['id']})

    # load all tags
    tags = self.data.fetch("tags")
    for tag in tags:
      # if tag is selected -- add a connection
      if tag[1] in selected_tags:
        self.data.insert("tags_hours", [tag[0], new_hour['id']])


  # def updateDisplayDay(self):
  #   """
  #   Updates the displayed date in the interface
  #   """
  #   self.hourLabel.setStringValue_(self.curr_time.strftime('%a %d %b, %I %p'))
  #   self.dayLabel.setStringValue_(self.curr_time.strftime('%a %d %b'))
  #   self.dayButton.setAttributedTitle_(self.curr_time.strftime('%a %d %b'))
  #   if self.reflection:
  #     self.dayField.setStringValue_(self.reflection)
  #     self.dayLabel.setTextColor_(NSColor.blackColor())
  #   else:
  #     self.dayField.setStringValue_('')
  #     self.dayLabel.setTextColor_(NSColor.redColor())
