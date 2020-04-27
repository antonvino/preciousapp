#!/usr/bin/python3

import PySimpleGUI as sg
from app import PreciousApp
from init_db import delete_tables

"""
Overall flow:

If sqlite database does not exist -- create it (this happens only once 
at the start of the app for the first time)
SQLite is the best because it's super simple and local. I can simply store the encrypted data there and decrypt it
once user puts in their password. (similar to how std notes do that)


Normal operation:

Open persistent window

Window shows current hour and date inviting to log with a textarea
Hashtag in the text adds a new tag for later use

Window loads your tags for hours (from db) and shows them as clickable buttons
If you click that button it adds it as hashtag into the text at current text pos

There is a selector of 3 buttons (good / neutral / bad) -- this is the core functionality to rate hours
This data will be used to plot graphs later

Log day window openable by a click of a button. Log day does the same thing as hour log just for a full day.
It's simply a separate table in db

Can click left/right to travel through hours of the day.
In this app we can have a "timetable" list on the left side as a column with all hours marked with certain colours 
E.g. grey -- not filled in

Hotkeys are a must
Ctrl + First: key of tag selects it
Enter: logs the hour
Ctrl + S: also logs the hour
Ctrl + Left arrow: move to prev hour
Ctrl + Right arrow: move to next hour


Plot icon-button opens the plot of your data -- it's a separate persistent window with different buttons
To be decided later


Closing main window closes app...



Right click on tags -> edit tags
Hides tags list, contents of textarea become tags which you can edit now
Save hour -> save tags
Extra button of different look says "Cancel"

Clicking on the Day label at the top
Changes the main textarea to the day's log text
Save hour -> Save day
Extra button of different look says "Edit hours"

View plot either opens new window or extends the window bottom and shows Canvas item with plots (to be decided)



Some issues with tags:
When you open the hour -- need to see already selected tags (take them out of text?)
Do we add tags to text? If we save twice they get added twice
Perhaps an easier way would be to just keep tags as a list, not in the text, 
but then would need to save tags in a separate field...

"""

class PreciousWindow():
  """
  Class for generic application functions
  """

  def __init__(self):
    self.app = PreciousApp()
    self.app.load_hour()

    # sg.theme('LightGrey1')
    # sg.theme('NeutralBlue')
    sg.theme('DarkBlue14')
    sg.theme_text_color('#c0c0c0')
    cols = sg.theme_button_color()
    sg.theme_button_color(tuple(['#c0c0c0', cols[1]]))
    sg.theme_element_text_color('#c0c0c0')
    sg.theme_input_text_color('#c0c0c0')

    if(self.app.hour_data['rating'] == -1):
      bad_button_init_color = ("#444444", "#bbbbbb")
      neutral_button_init_color = sg.theme_button_color()
      good_button_init_color = sg.theme_button_color()
    if(self.app.hour_data['rating'] == 0):
      bad_button_init_color = sg.theme_button_color()
      neutral_button_init_color = ("#444444", "#bbbbbb")
      good_button_init_color = sg.theme_button_color()
    if(self.app.hour_data['rating'] == 1):
      bad_button_init_color = sg.theme_button_color()
      neutral_button_init_color = sg.theme_button_color()
      good_button_init_color = ("#444444", "#bbbbbb")


    temp_hours = (' 1 PM', ' 2 PM', ' 3 PM', ' 4 PM', ' 5 PM', ' 6 PM', ' 7 PM', ' 8 PM', ' 9 PM', ' 10 PM', ' 11 PM')

    # hour list column
    column1 = [
      [sg.Listbox(
        values=temp_hours, 
        size=(10, 12), 
        enable_events=True, 
        key="select_hour", 
        background_color=sg.theme_background_color(), 
        no_scrollbar=True)], #, sg.VerticalSeparator()],
    ]

    # main column
    column2 = [
      # the hour switch row
      [
        sg.Button('←', key="prev_hour", font="Roboto 12 normal", size=(4,1)), 
        sg.Button(
          self.app.get_hour_label(), 
          key="open_day", 
          size=(18,1), 
          pad=((65, 0), (0, 0)), 
          button_color=(sg.theme_text_color(), 
          sg.theme_background_color()), 
          border_width=0, 
          font='Roboto 12 underline'
        ), 
        sg.Button('→', key="next_hour", font="Roboto 12 normal", pad=((65, 0), (0, 0)), size=(4,1)),
      ],

      # the rating row
      [
        sg.Button('Bad',     key="bad",     font="Roboto 10 normal", size=(4,1), pad=((230, 0), (10, 0)), button_color=bad_button_init_color ),
        sg.Button('Neutral', key="neutral", font="Roboto 10 normal", size=(4,1), pad=((0, 0),   (10, 0)), button_color=neutral_button_init_color ), 
        sg.Button('Good',    key="good",    font="Roboto 10 normal", size=(4,1), pad=((0, 0),   (10, 0)), button_color=good_button_init_color )
      ],

      # the textarea and tag row
      [
        sg.Multiline(
          default_text=self.app.get_hour_text(), 
          size=(30, 6), 
          key="hour_text", 
          pad=((5, 0), (15, 0)), 
          do_not_clear=True, focus=True, 
          background_color=sg.theme_background_color() 
        ),
        sg.Listbox(
          values=self.app.get_tags("#"), 
          size=(15, 6), 
          enable_events=False, 
          key="select_tag", 
          select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
          background_color=sg.theme_background_color(), 
          pad=((5, 0), (15, 0)), 
          no_scrollbar=False, 
          right_click_menu = ['!Tags', ['!Tags', '&Edit tags::edit_tags']]
        )
      ],

      # the action button row
      [
        sg.Button('Save hour', key="save", font="Roboto 10 normal", size=(8,1), pad=((5, 0), (15, 0))), 
        sg.Text('', key="status", size=(24,1), pad=((10, 0), (10, 0))),
        sg.Button('View plot', key="open", font="Roboto 10 normal", size=(8,1), pad=((10, 0), (15, 0))), 
      ]
    ]

    # All the stuff inside the window
    layout = [ 
      [
        # sg.Column(column1),
        sg.Column(column2)
      ]
    ]

    self.edit_tags = False
    self.curr_rating = 0

    # Create the Window
    self.window = sg.Window('My time is precious', layout, font='Roboto 10 normal')


  def update_hour(self):
    hour_label = self.window["open_day"]
    hour_label.Update(text=self.app.get_hour_label())

    hour_text = self.window["hour_text"]
    hour_text.Update(value=self.app.get_hour_text())

    self.update_rating(self.app.hour_data['rating'])


  def to_prev_hour(self):
    self.app.to_prev_hour()
    self.app.load_hour()
    self.app.load_time(self.app.hour_data['timestamp'])
    self.update_hour()


  def to_next_hour(self):
    self.app.to_next_hour()
    self.app.load_hour()
    self.app.load_time(self.app.hour_data['timestamp'])
    self.update_hour()


  def update_rating(self, rating):
    if(rating == -1):
      bad_button_color = ("#444444", "#bbbbbb")
      neutral_button_color = sg.theme_button_color()
      good_button_color = sg.theme_button_color()
    if(rating == 0):
      bad_button_color = sg.theme_button_color()
      neutral_button_color = ("#444444", "#bbbbbb")
      good_button_color = sg.theme_button_color()
    if(rating == 1):
      bad_button_color = sg.theme_button_color()
      neutral_button_color = sg.theme_button_color()
      good_button_color = ("#444444", "#bbbbbb")

    bad_button = self.window["bad"]
    bad_button.Update(button_color=bad_button_color)
    neutral_button = self.window["neutral"]
    neutral_button.Update(button_color=neutral_button_color)
    good_button = self.window["good"]
    good_button.Update(button_color=good_button_color)

    self.curr_rating = rating

  
  def save(self, values):

    # edit hour
    if not self.edit_tags:
      self.app.save_hour(values['hour_text'], self.curr_rating, values['select_tag'])
      self.update_hour()

    else: # edit tags
      tags = values['hour_text'].split(", #")
      valid_tags = []
      for tag in tags:
        tag = tag.replace("#", "").replace("\n","")
        if len(tag) > 0:
          valid_tags.append(tag)
      
      self.app.save_tags(valid_tags)

      open_button = self.window["status"]
      open_button.Update(value="Tags saved.")

      self.cancel_edit_tags()
      self.update_hour()


  def start_edit_tags(self):
    tags_listbox = self.window["select_tag"]
    tags_listbox.Update(disabled=True)

    hour_text = self.window["hour_text"]

    strval = ""
    for tag in self.app.get_tags():
      strval += "#{0}, ".format(tag)

    strval += "#" # prompt new tag
    hour_text.Update(value=strval)

    save_button = self.window["save"]
    save_button.Update(text="Save tags")

    open_button = self.window["open"]
    open_button.Update(text="Cancel")

    self.edit_tags = True


  def cancel_edit_tags(self):
    tags_listbox = self.window["select_tag"]
    tags_listbox.Update(disabled=False)

    hour_text = self.window["hour_text"]
    hour_text.Update(value="Load hour data again")

    save_button = self.window["save"]
    save_button.Update(text="Save hour")

    open_button = self.window["open"]
    open_button.Update(text="View plot")

    tags_listbox = self.window["select_tag"]
    tags_listbox.Update(values=self.app.get_tags())

    self.edit_tags = False


if __name__ == "__main__":

  # delete_tables("data.db")

  w = PreciousWindow()

  # Event Loop to process "events" and get the "values" of the inputs
  while True:
    event, values = w.window.read()
    if event in (None, 'Cancel'):   # if user closes window or clicks cancel
      break

    elif event == 'select_hour':
      print("Hour selected: {0}".format(values['select_hour']))

    # open day window
    elif event == 'open_day':
      # event, values  = sg.Window('SHA-1 & 256 Hash', [[sg.Text('SHA-1 and SHA-256 Hashes for the file')],
      #                         [sg.InputText(), sg.FileBrowse()],
      #                         [sg.Submit(), sg.Cancel()]]).read(close=True)
      # source_filename = values[0]    
      pass

    elif event == 'prev_hour':
      w.to_prev_hour()

    elif event == 'next_hour':
      w.to_next_hour()

    elif event == 'Edit tags::edit_tags':
      w.start_edit_tags()

    elif event == 'open':

      if w.edit_tags:
        w.cancel_edit_tags()
      else:
        print("TODO: open plot")

    elif event == "save":
      w.save(values)

    elif event == "bad":
      w.update_rating(-1)

    elif event == "neutral":
      w.update_rating(0)

    elif event == "good":
      w.update_rating(1)

    else:
      print("Unknown event")
      print(event)
      print(values)

    # print('You entered ', values[0])
    # print(values)

  w.window.close()