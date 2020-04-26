#!/usr/bin/python3
import time
from datetime import datetime, timedelta, date

class PreciousApp:
  """
  Class for generic application functions
  """

  def __init__(self):
    self.get_current_time()

  def get_current_time(self):
    """
    Takes current timestamp and updates the date/time data
    """
    self.curr_time = datetime.fromtimestamp(time.time())
    self.year = self.curr_time.year
    self.month = self.curr_time.month
    self.day = self.curr_time.day
    self.hour = int(self.curr_time.strftime('%H')) # need a 24 hour   
    return self.curr_time     

  def get_hour_label(self, label_time):
    return label_time.strftime('%a %d %b, %I %p')
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

  def updateDisplayDay(self):
    """
    Updates the displayed date in the interface
    """
    self.hourLabel.setStringValue_(self.curr_time.strftime('%a %d %b, %I %p'))
    self.dayLabel.setStringValue_(self.curr_time.strftime('%a %d %b'))
    self.dayButton.setAttributedTitle_(self.curr_time.strftime('%a %d %b'))
    if self.reflection:
      self.dayField.setStringValue_(self.reflection)
      self.dayLabel.setTextColor_(NSColor.blackColor())
    else:
      self.dayField.setStringValue_('')
      self.dayLabel.setTextColor_(NSColor.redColor())

  def switchDate(self):
    """
    Loads the hour & day data and calls display update
    """
    # get the time data
    self.reloadTime()
    # load the data
    self.clearData()
    self.loadData(
      year = self.curr_time.year,
      month = self.curr_time.month,
      day = self.curr_time.day,
      hour = self.curr_time.hour)
    # update the interface
    self.updateDisplayDay()
    self.updateDisplayHour()  