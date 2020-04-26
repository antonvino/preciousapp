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


  def to_prev_hour(self):
    self.load_time(self.curr_timestamp - 3600)


  def to_next_hour(self):
    self.load_time(self.curr_timestamp + 3600)


  def get_hour_text(self):
    self.data.fetch("hours", datetime) # timestamp...


  def get_tags(self):
    tags = []
    data = self.data.fetch("tags")
    print(data)
    for tag in data:
      tags.append("# {0}".format(tag[0]))
    return tags


  def save_tags(self, tags):
    self.data.delete_all("tags")
    db_tags = []
    for tag in tags:
      db_tags.append({"name": tag})
    self.data.insert_many("tags",db_tags)

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

  # def switchDate(self):
  #   """
  #   Loads the hour & day data and calls display update
  #   """
  #   # get the time data
  #   self.reloadTime()
  #   # load the data
  #   self.clearData()
  #   self.loadData(
  #     year = self.curr_time.year,
  #     month = self.curr_time.month,
  #     day = self.curr_time.day,
  #     hour = self.curr_time.hour)
  #   # update the interface
  #   self.updateDisplayDay()
  #   self.updateDisplayHour()  