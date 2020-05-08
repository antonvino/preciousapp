#!/usr/bin/python3

import PySimpleGUI as sg
from app import PreciousApp
from init_db import delete_tables
from get_icon import get_icon
from time import sleep

"""
Overall flow:

If sqlite database does not exist -- create it (this happens only once 
at the start of the app for the first time)
SQLite is the best because it's super simple and local. Can store the encrypted data there and decrypt it
once user puts in their password (similar to how std notes do that)

---

Normal operation:


Open one persistent window
Window shows current hour and date inviting to log with a textarea
This window loads the hour if it has been logged already (if you already logged this hour -- you just see what you wrote)

--- 

Window loads and shows all of your tags for hours (from db) and shows them as clickable buttons
If you click that button it adds a tag to the hour log
(currently they are added as #-tags but can consider just adding 
connections in DB and displaying in the list or separate area to the text)

TODO: Show the selected tags at the top of the list (sort)
TODO: When hour is loaded -- load saved tags, highlight the selected tags (i.e. pre-select them)
TODO: Decide how to save tags (separate text field? separate table that connects hours-tags? 
      Approx 9000+ hours per year so lookup is not too bad even if we just store tags in the text and search for them
      when searching for hours with certain tags
TODO: sort tags with most used at the top


---

There is a selector of 3 buttons (good / neutral / bad) -- this is the core functionality to rate hours
This data will be used to plot graphs later

---

Log day window openable by a click on the day in the label (or other button?). 
Log day does the same thing as hour log just for a full day, it's simply a separate table in db

---

OLD: Can click left/right arrow buttons in the window to travel through hours of the day.
In this app we can have a "timetable" list on the left side as a column with all hours marked with certain colours 
E.g. grey -- not filled in
The list of hours should be the primary navigation between hours it's nicer!

---

Hotkeys are a must
Ctrl + First: key of tag selects it
Enter: logs the hour
Ctrl + S: also logs the hour
Ctrl + Up arrow: move to prev hour
Ctrl + Down arrow: move to next hour

---

Plot icon-button opens the plot of your data -- it's a separate persistent window with different buttons
To be decided later
"View plot" button either opens new window or extends the window bottom and shows Canvas item with plots (to be decided)

---

Right click on tags -> edit tags
Hides tags list, contents of textarea become tags which you can edit now
Save hour -> save tags
Extra button of different look says "Cancel" -- that closes tags editing without saving

---

Clicking on the Day label at the top
Changes the main textarea to the day's log text
Save hour -> Save day (this button saves the day log)
Extra button of different look says "Back to edit hours" -- which goes back to hour editing and does not save day log

---

Closing main window closes app...

---

Hour list
"Center" list at the current hour shown i.e. the 6-th element in the list is that.
Above are the earlier hours in the day all the way up to where the day changes to the previous day
Below are the later hours in the day all the way up to where the day changes to the next day

If hours are in the future from current date -- they are shown disabled
If hours are not logged yet -- they are shown as "bold" or other colour inviting to log
Logged hours are shown in normal font -- i.e. not inviting

Once you navigated all the way to the top you see a Day label which when clicked moves the view to the previous day.
Same for navigating to the bottom

Scroll should work to scroll to the top/bottom but to switch the day once has to click the day label.

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
    # sg.theme('Default')

    sg.theme_background_color('#0f3c3b')
    sg.theme_text_color('#59bdbb')
    # cols = sg.theme_button_color()
    sg.theme_button_color(tuple(['#93c6c5', '#008382']))
    sg.theme_element_text_color('#59bdbb')
    sg.theme_input_text_color('#59bdbb')
    sg.theme_text_element_background_color('#0f3c3b')
    sg.theme_element_background_color('#0f3c3b')

    empty_button_color = (sg.theme_background_color(), sg.theme_background_color())

    if(self.app.hour_data['rating'] == -1):
      bad_button_init_color = ("#222222", "#93c6c5")
      neutral_button_init_color = sg.theme_button_color()
      good_button_init_color = sg.theme_button_color()
    if(self.app.hour_data['rating'] == 0):
      bad_button_init_color = sg.theme_button_color()
      neutral_button_init_color = ("#222222", "#93c6c5")
      good_button_init_color = sg.theme_button_color()
    if(self.app.hour_data['rating'] == 1):
      bad_button_init_color = sg.theme_button_color()
      neutral_button_init_color = sg.theme_button_color()
      good_button_init_color = ("#222222", "#93c6c5")

    column1 = [
      [sg.Button("Now", key="now", size=(5,1), font='Roboto 11', border_width=0, pad=((5, 5), (5, 20)) )],
      [sg.Button(u'\N{BLACK UP-POINTING TRIANGLE}',   key="prev",  size=(5,1), font='Roboto 12', button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0, pad=((5, 5), (5, 5)) )]
    ]

    for i in range(-3,4):
      hour = self.app.get_time(self.app.curr_timestamp + 3600 * i)

      color = (sg.theme_text_color(), sg.theme_background_color())
      if i == 0:
        color = sg.theme_button_color()

      if i < 0:
        key = "hour_dec_{0}".format(abs(i))
      elif i > 0:
        key = "hour_inc_{0}".format(abs(i))
      else:
        key = "hour_current"

      column1.append(
        [sg.Button(
          self.app.get_hour_short_label(hour['time']), 
          key = key, 
          # size=(18,1), 
          # pad=((65, 0), (0, 0)), # 140+65 when arrow keys are off 
          button_color=color, 
          border_width=0, 
          font='Roboto 11'
        )] 
      )

    column1.append(
      [sg.Button(u'\N{BLACK DOWN-POINTING TRIANGLE}', key="next", size=(5,1), font='Roboto 12', button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0, pad=((5, 5), (5, 5)) )]
    )
    # hour list column
    # column1 = [
    #   hour_list
      # [sg.Listbox(
      #   values=temp_hours, 
      #   size=(10, 12), 
      #   enable_events=True, 
      #   key="select_hour", 
      #   background_color=sg.theme_background_color(), 
      #   no_scrollbar=False)],
    # ]

    # main column
    column2 = [
      [
        sg.Text(
          self.app.get_hour_label(), 
          key="current", 
          size=(21,1), 
          # background_color="#555555",
          justification='left',
          font='Roboto 17 normal',
          pad=((10, 5), (5, 5))
        ),
        # sg.Text("", size=(40,1)),
        sg.Button("Log day",   key="day",  border_width=0, pad=((5, 5), (5, 5))), 
        sg.Button("View plot", key="plot", border_width=0, pad=((5, 5), (5, 5)))
      ],
      # [sg.Text("", font='Roboto 6 normal', size=(40,1))],

      # the rating row
      [
        sg.Button('Bad',     key="bad",     font="Roboto 11 normal", size=(5,1), pad=((5, 0), (10, 5)), border_width=0, button_color=bad_button_init_color ),
        sg.Button('Neutral', key="neutral", font="Roboto 11 normal", size=(5,1), pad=((0, 0), (10, 5)), border_width=0, button_color=neutral_button_init_color ), 
        sg.Button('Good',    key="good",    font="Roboto 11 normal", size=(5,1), pad=((0, 0), (10, 5)), border_width=0, button_color=good_button_init_color )
      ],

      # the textarea and tag row
      [
        sg.Multiline(
          default_text=self.app.get_hour_text(), 
          size=(30, 10), 
          key="hour_text", 
          pad=((5, 0), (15, 5)), 
          do_not_clear=True, focus=True, 
          background_color='#005e5c',
          text_color='#93c6c5',
          border_width=0,
          font="Roboto 11 normal"
        ),
        # sg.Text("", size=(5,1)),
        sg.Listbox(
          values=self.app.get_tags("#"), 
          size=(20, 10), 
          enable_events=False, 
          key="select_tag", 
          select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
          background_color=sg.theme_background_color(), 
          pad=((5, 0), (15, 5)), 
          no_scrollbar=False, 
          font="Roboto 11 normal",
          right_click_menu = ['!Tags', ['!Tags', '&Edit tags::edit_tags']]
        )
      ],

      # the action button row
      [
        sg.Text('', justification="left", key="status", size=(28,1), pad=((10, 10), (15, 0)), text_color='#f0f056'),
        sg.Button('', key="cancel", font="Roboto 11 normal", border_width=0, size=(9,1), pad=((10, 0), (15, 0)), button_color=empty_button_color), 
        sg.Button('Save hour', key="save", font="Roboto 11 normal", border_width=0, size=(8,1), pad=((5, 0), (15, 0))), 
      ],
    ]

    # All the stuff inside the window
    layout = [ 
      [
        sg.Column(
          column1, 
          element_justification='center',
          # size=(150,600)
        ),
        sg.VerticalSeparator(),
        sg.Column(
          column2, 
          justification='center', 
          element_justification='left',
          # size=(910,600), 
          pad=((20,5),(5,5)), 
        )
      ]
    ]

    self.edit_tags = False
    self.curr_rating = 0

    # Create the Window
    self.window = sg.Window(
      'Precious', 
      layout, 
      font='Roboto 11 normal',
      resizable=False, 
      location=(2400,200),
      finalize=True,
      # element_justification='left'
      # use_ttk_buttons = True
    )
    self.window.set_icon(None, get_icon())


  def update_hour(self):
    hour_label = self.window["current"]
    hour_label.Update(value=self.app.get_hour_label())

    hour_text = self.window["hour_text"]
    hour_text.Update(value=self.app.get_hour_text())

    self.update_rating(self.app.hour_data['rating'])
    self.update_tags("hour", self.app.hour_data['id'])


  def update_rating(self, rating):
    if(rating == -1):
      bad_button_color = ("#222222", "#93c6c5")
      neutral_button_color = sg.theme_button_color()
      good_button_color = sg.theme_button_color()
    if(rating == 0):
      bad_button_color = sg.theme_button_color()
      neutral_button_color = ("#222222", "#93c6c5")
      good_button_color = sg.theme_button_color()
    if(rating == 1):
      bad_button_color = sg.theme_button_color()
      neutral_button_color = sg.theme_button_color()
      good_button_color = ("#222222", "#93c6c5")

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

      text_tags = values['hour_text'].split(" #")
      valid_tags = []
      for i,tag in enumerate(text_tags):
        if i > 0:
          tag = tag.replace(",", "").replace("#", "").replace("\n","")
          if len(tag) > 0:
            valid_tags.append(tag)

      if(len(valid_tags) > 0):
        self.app.add_tags(valid_tags)

      tags = values['select_tag']
      for i, tag in enumerate(tags):
        tags[i] = tag.replace("#", "")

      # merge list
      tags = tags + valid_tags

      text = values['hour_text']
      # saving textarea always gives an extra newline so let's delete it
      if text.find("\n", len(text)-1, len(text)) != -1:
        text = text[0:len(text)-1]

      self.app.save_hour(text, self.curr_rating, tags)
      self.update_hour()
      
      status = self.window["status"]
      status.Update(value="Hour saved.")
      self.window.Finalize()
      sleep(0.7)
      status.Update(value="")


    else: # edit tags
      tags = values['hour_text'].split(", #")
      valid_tags = []
      for tag in tags:
        tag = tag.replace(",", "").replace("#", "").replace("\n","")
        if len(tag) > 0:
          valid_tags.append(tag)
      self.app.save_tags(valid_tags)

      status = self.window["status"]
      status.Update(value="Tags saved.")
      self.window.Finalize()
      sleep(0.5)
      status.Update(value="")

      self.cancel_edit_tags()
      self.update_hour() # reload hour data


  def update_tags(self, item, id):
    # tags = self.window['select_tag'].get_list_values()
    tags = self.app.get_tags("#")
    self.window['select_tag'].Update(values=tags)

    attached_tags = self.app.get_item_tags(item, id)

    indexes = []
    for i,tag in enumerate(tags):
      tag = tag.replace("#", "")
      if(tag in attached_tags):
        indexes.append(i)    

    self.window['select_tag'].Update(set_to_index=indexes)


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

    open_button = self.window["cancel"]
    open_button.Update(text="Cancel", button_color=(sg.theme_text_color(), sg.theme_background_color()))

    self.edit_tags = True


  def cancel_edit_tags(self):
    tags_listbox = self.window["select_tag"]
    tags_listbox.Update(disabled=False)

    hour_text = self.window["hour_text"]
    hour_text.Update(value="Load hour data again")

    save_button = self.window["save"]
    save_button.Update(text="Save hour")

    open_button = self.window["cancel"]
    open_button.Update(text="", button_color=(sg.theme_background_color(), sg.theme_background_color()))

    tags_listbox = self.window["select_tag"]
    tags_listbox.Update(values=self.app.get_tags())

    self.edit_tags = False


  def current_hour(self):
    self.app.load_current_time()
    self.app.load_hour()
    self.change_hour("now", 0)


  def change_hour(self, label, change):

    # animation delay
    delay = abs(change)
    if delay == 0:
      delay = 5 # to load "now" -- have a longer delay

    labels = {
      # "hour_dec_4": -4,
      "hour_dec_3": -3,
      "hour_dec_2": -2,
      "hour_dec_1": -1,
      # "hour_current",
      "hour_inc_1": 1,
      "hour_inc_2": 2,
      "hour_inc_3": 3,
      # "hour_inc_4": 4,
    }
    self.animation_hide(labels.keys(), delay)

    self.app.change_hour(change)
    self.app.load_hour()
    self.app.load_time(self.app.hour_data['timestamp'])
    self.update_hour()

    for label,dt in labels.items():
      # dt = i - round(len(labels)/2)
      # print(dt)
      hour = self.app.get_time(self.app.curr_timestamp + 3600 * dt)
      # labels[label] = hour['time']
      self.window[label].Update(text=self.app.get_hour_short_label(hour['time']))

    self.window["hour_current"].Update(text=self.app.get_hour_short_label())

    self.animation_show(labels.keys(), delay)

    # for i in range(-4,5):
    #   hour = self.app.get_time(self.app.curr_timestamp + 3600 * i)

    #   color = (sg.theme_text_color(), sg.theme_background_color())
    #   if i == 0:
    #     color = sg.theme_button_color()

    #   if i < 0:
    #     key = "hour_dec_{0}".format(abs(i))
    #   elif i > 0:
    #     key = "hour_inc_{0}".format(abs(i))
    #   else:
    #     key = "hour_current"

    #   self.window['hour_' + ]
    #   column1.append(
    #     [sg.Button(
    #       self.app.get_hour_short_label(hour['time']), 
    #       key = key, 
    #       # size=(18,1), 
    #       # pad=((65, 0), (0, 0)), # 140+65 when arrow keys are off 
    #       button_color=color, 
    #       border_width=0, 
    #       font='Roboto 11'
    #     )] 
    #   )



  def animation_hide(self, labels, delay):
    if delay < 2:
      return False

    anim_colors = [
      sg.theme_text_color(),
      "#999999",
      "#888888",
      "#777777",
      "#666666",
      "#555555",
      "#222222",
      "#333333",
      sg.theme_background_color()
    ]
    for col in anim_colors:
      for label in labels:
        self.window[label].Update(button_color=(col, sg.theme_background_color()))
      self.window.Finalize()
      sleep(0.005 * float(delay))


  def animation_show(self, labels, delay):
    if delay < 2:
      return False

    anim_colors = [
      sg.theme_background_color(),
      "#333333",
      "#222222",
      "#555555",
      "#666666",
      "#777777",
      "#888888",
      "#999999",
      sg.theme_text_color()
    ]
    for col in anim_colors:
      for label in labels:
        self.window[label].Update(button_color=(col, sg.theme_background_color()))
      self.window.Finalize()
      sleep(0.005 * float(delay))




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

    elif event == 'hour_current':
      # print(w.window.current_location())
      w.change_hour(event, 0)

    elif event == 'now':
      w.current_hour()      

    elif event == 'prev':
      w.change_hour(event, -1)

    elif event == 'next':
      w.change_hour(event, +1)

    elif event == 'Edit tags::edit_tags':
      w.start_edit_tags()

    elif event == 'cancel':

      if w.edit_tags:
        w.cancel_edit_tags()
      else:
        print("NOTHING")

    elif event == "save":
      w.save(values)

    elif event == "bad":
      w.update_rating(-1)

    elif event == "neutral":
      w.update_rating(0)

    elif event == "good":
      w.update_rating(1)

    elif event.find("hour_dec_") != -1:
      w.change_hour(event, (-1) * int(event.replace("hour_dec_","")))

    elif event.find("hour_inc_") != -1:
      w.change_hour(event, int(event.replace("hour_inc_","")))

    else:
      print("Unknown event")
      print(event)
      print(values)

    # print('You entered ', values[0])
    # print(values)

  w.window.close()