#!/usr/bin/python3

import PySimpleGUI as sg
from app import PreciousApp
from init_db import reset_db
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

---

There is a selector of 3 buttons (good / neutral / bad) -- this is the core functionality to rate hours
This data will be used to plot graphs later

---

Log day window openable by a click on the day in the label (or other button -- UPD: menu). 
Log day does the same thing as hour log just for a full day, it's simply a separate table in db

---

In this app we can have a "timetable" list on the left side as a column with all hours marked with certain colours 
E.g. grey -- not filled in
The list of hours should be the primary navigation between hours it's nicer!

---

Hotkeys
Ctrl + First: key of tag selects it
Enter/Space/.: logs the hour
Up arrow: move to prev hour
Down arrow: move to next hour

---

Plot icon-button opens the plot of your data -- it's a separate persistent window with different buttons
To be decided later
"View plot" button either opens new window or extends the window bottom and shows Canvas item with plots (to be decided)

---

Edit tags in menu
Replaces tags with inputs
Extra button of different look says "Cancel" -- that closes tags editing without saving

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

    # default variables
    self.edit_tags = False
    self.curr_rating = 0
    self.menu_visible = False
    self.selected_tags = []

    # base theme
    sg.theme('DarkBlue14')
    # my own theme modifications
    sg.SetOptions(
      # icon=None,
      button_color=('#93c6c5', '#008382'),
      margins=(0, 0),
      font='Roboto 12 normal',
      border_width=0,
      slider_border_width=0,
      slider_relief=0,
      message_box_line_width=0,
      progress_meter_border_depth=0,
      background_color='#0f3c3b',
      element_background_color='#0f3c3b',
      text_element_background_color='#0c2d2c',
      input_elements_background_color='#0f3c3b',
      input_text_color='#59bdbb',
      scrollbar_color='#0f3c3b',
      text_color='#59bdbb',
      element_text_color='#59bdbb'
    )

    # tag colors to create an illusion of buttons
    self.tag_hash_color = "#666666"
    self.tag_text_color = "#59bdbb" 
    self.tag_background_color = "#0c2d2c"
    self.tag_selected_text_color = "#93c6c5" 
    self.tag_selected_background_color = "#008382"

    # other colors
    self.empty_button_color = (sg.theme_background_color(), sg.theme_background_color())
    self.dark_column_background_color = "#0c2d2c"
    self.rating_selected_text_color = "#222222"
    self.rating_selected_background_color = "#93c6c5"

    # hour selections column
    column1 = [
      [sg.Button("Now", key="now", size=(5,1), font='Roboto 14 normal', border_width=0, pad=((5, 5), (15, 5)) )],
      [sg.Button(u'\N{BLACK UP-POINTING TRIANGLE}',   key="prev",  size=(5,1), font='Roboto 16', button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0, pad=((5, 5), (5, 5)) )]
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
          button_color=color, 
          border_width=0, 
          font='Roboto 12'
        )] 
      )

    column1.append(
      [sg.Button(u'\N{BLACK DOWN-POINTING TRIANGLE}', key="next", size=(5,1), font='Roboto 16', button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0, pad=((5, 5), (5, 5)) )]
    )

    # init rating buttons
    if(self.app.hour_data['rating'] == -1):
      bad_button_init_color = (self.rating_selected_text_color, self.rating_selected_background_color)
      neutral_button_init_color = sg.theme_button_color()
      good_button_init_color = sg.theme_button_color()
    if(self.app.hour_data['rating'] == 0):
      bad_button_init_color = sg.theme_button_color()
      neutral_button_init_color = (self.rating_selected_text_color, self.rating_selected_background_color)
      good_button_init_color = sg.theme_button_color()
    if(self.app.hour_data['rating'] == 1):
      bad_button_init_color = sg.theme_button_color()
      neutral_button_init_color = sg.theme_button_color()
      good_button_init_color = (self.rating_selected_text_color, self.rating_selected_background_color)

    # init load tags
    tags = self.app.get_tags()
    attached_tags = self.app.get_item_tags("hour", self.app.hour_data['id'])
    select_tags_layout = []
    edit_tags_layout = []
    self.selected_tags = []
    for tag in tags:
      if(tag['id'] in attached_tags):
        self.selected_tags.append(tag['id'])
        text_color = self.tag_selected_text_color
        bg_color = self.tag_selected_background_color
      else:
        text_color = self.tag_text_color
        bg_color = self.tag_background_color
      
      select_tags_layout.append(
        [
          sg.Text("#",         pad=((5,0),(5,5)), key="hash_tag" + str(tag['id']),   text_color=self.tag_hash_color, background_color=bg_color, enable_events=True), 
          sg.Text(tag['name'], pad=((0,5),(5,5)), key="select_tag" + str(tag['id']), text_color=text_color,          background_color=bg_color, enable_events=True)
        ]
      )
      edit_tags_layout.append(
        [sg.Text("#", text_color=self.tag_hash_color, pad=((5,0),(5,5)) ), sg.InputText(tag['name'], size=(17,1), key="edit_tag" + str(tag['id']))],
      )

    # both select and edit tags need a line at the end to center tags over the whole column width
    select_tags_layout.append([sg.Text("", size=(27,1))])
    # edit tags needs buttons
    edit_tags_layout.append([sg.Button("cancel", key="cancel_edit_tags"), sg.Button("save tags", key="save_tags")])
    edit_tags_layout.append([sg.Text("", size=(27,1))])

    # main column
    column2 = [
      [
        sg.Text(
          self.app.get_hour_label(), 
          key="current", 
          size=(17,1), 
          # background_color="#555555",
          justification='center',
          font='Roboto 16 normal',
          pad=((25, 5), (15, 5))
        ),
        sg.Button(
          u'\u2630', 
          key="menu", 
          border_width=0, 
          size=(1,1),
          font='Roboto 14',
          button_color=(sg.theme_text_color(), sg.theme_background_color()), 
          pad=((5, 5), (15, 5))
        )
      ],

      # the rating row
      [
        sg.Button('Bad',     key="bad",     font="Roboto 12 normal", size=(6,1), pad=((15, 0), (15, 5)), border_width=0, button_color=bad_button_init_color ),
        sg.Button('Neutral', key="neutral", font="Roboto 12 normal", size=(8,1), pad=((0, 0),  (15, 5)), border_width=0, button_color=neutral_button_init_color ), 
        sg.Button('Good',    key="good",    font="Roboto 12 normal", size=(6,1), pad=((0, 15),  (15, 5)), border_width=0, button_color=good_button_init_color )
      ],

      # the textarea and tag row
      [
        sg.Multiline(
          default_text=self.app.get_hour_text(), 
          size=(27, 5), 
          key="hour_text", 
          pad=((25, 25), (15, 5)), 
          do_not_clear=True, focus=True, 
          background_color='#005e5c',
          text_color='#93c6c5',
          border_width=0,
          # enable_events=True,
        ),
      ],

      [
        # tag selection column (shown by default)
        sg.Column(
          layout=select_tags_layout,
          # [
          #   [sg.Text("#", text_color=self.tag_hash_color, pad=((5,0),(5,5)) ), sg.Text("work", key="ttag1")],
          #   [sg.Text("#", text_color=self.tag_hash_color, pad=((5,0),(5,5)), background_color='#008382' ), sg.Text("self-development", pad=((0,0),(5,5)), key="ttag2", background_color='#008382')],
          #   [sg.Text("#", text_color=self.tag_hash_color, pad=((5,0),(5,5)) ), sg.Text("sport", key="ttag3")],
          #   [sg.Text("#", text_color=self.tag_hash_color, pad=((5,0),(5,5)) ), sg.Text("family", key="ttag4")],
          #   [sg.Text("#", text_color=self.tag_hash_color, pad=((5,0),(5,5)) ), sg.Text("friends", key="ttag5")],
          #   [sg.Text("", size=(27,1))],
          # ],
          background_color=self.dark_column_background_color,
          pad=((25, 25), (15, 5)),
          key="tags_click",
          visible=True,
          element_justification='center'
        ),
        # tag editing column (shown when editing)
        sg.Column(
          layout=edit_tags_layout,
          # [
          #   [sg.Text("#", text_color=self.tag_hash_color, pad=((5,0),(5,5)) ), sg.InputText("work", size=(17,1), key="tag0")],
          #   [sg.Text("#", text_color=self.tag_hash_color, pad=((5,0),(5,5)) ), sg.InputText("self-development", size=(17,1), key="tag1")],
          #   [sg.Text("#", text_color=self.tag_hash_color, pad=((5,0),(5,5)) ), sg.InputText("sport", size=(17,1), key="tag2")],
          #   [sg.Text("#", text_color=self.tag_hash_color, pad=((5,0),(5,5)) ), sg.InputText("family", size=(17,1), key="tag3")],
          #   [sg.Text("#", text_color=self.tag_hash_color, pad=((5,0),(5,5)) ), sg.InputText("friends", size=(17,1), key="tag4")],
          #   [sg.Button("cancel", key="cancel_edit_tags"), sg.Button("save tags", key="save_tags")],
          #   [sg.Text("", size=(27,1))],
          # ],
          background_color=self.dark_column_background_color,
          pad=((25, 25), (15, 5)),
          key="tags_edit",
          visible=False,
          element_justification='center'
        )
      ],
    ]

    # menu column
    column3 = [
      [sg.Text("", justification='left', font='Roboto 16 normal', background_color=sg.theme_background_color(), pad=((5,5),(15,5)) )],
      [sg.Button("view plot",   key="plot",      button_color=(sg.theme_text_color(), sg.theme_background_color()))],
      [sg.Button("review days", key="log_days",  button_color=(sg.theme_text_color(), sg.theme_background_color()))],
      [sg.Button("edit tags",   key="edit_tags", button_color=(sg.theme_text_color(), sg.theme_background_color()))],
      [sg.Text("-" * 18, size=(14,1), justification='center', background_color=sg.theme_background_color() )],
      [sg.Checkbox("dark mode", default=True)],
      [sg.Checkbox("24 hour mode", disabled=True)],
      [sg.Checkbox("encryption", disabled=True)],
      [sg.Checkbox("tip of the day", disabled=True)],
    ]

    # columns of the main window
    layout = [ 
      [
        sg.Column(
          column1, 
          element_justification='center',
          pad=((0,0),(0,0)), 
        ),
        sg.Column(
          column2, 
          background_color=self.dark_column_background_color,
          element_justification='center',
          pad=((0,0),(0,0)), 
        ),
        sg.Column(
          column3,
          key="menu_column",
          element_justification='left',
          pad=((0,0),(0,0)),
          visible=self.menu_visible
        ),
      ]
    ]

    # Create the Window
    self.window = sg.Window(
      'Precious', 
      layout, 
      font='Roboto 12 normal',
      resizable=False, 
      location=(200,200),
      finalize=True,
      return_keyboard_events = False,
      # use_default_focus=False
      # element_justification='left'
      # use_ttk_buttons = True
    )

    # icon for the app (TODO: test)
    self.window.set_icon(None, get_icon())

    self.window.bind("<Up>", "prev")
    self.window.bind("<Down>", "next")

    self.window['hour_text'].bind("<space>","")
    self.window['hour_text'].bind("<Return>","")
    self.window['hour_text'].bind(".","")
    # self.window['hour_text'].bind("<Leave>","")
    

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
        
    # Note: this is tag adding from text part
    # currently not used as I keep the same amount of tags
    # edit hour
    # text_tags = values['hour_text'].split(" #")
    # valid_tags = []
    # for i,tag in enumerate(text_tags):
    #   if i > 0:
    #     tag = tag.replace(",", "").replace("#", "").replace("\n","")
    #     if len(tag) > 0:
    #       valid_tags.append(tag)

    # if(len(valid_tags) > 0):
    #   self.app.add_tags(valid_tags)
    # merge list
    # tags = tags + valid_tags

    text = values['hour_text']
    # saving textarea always gives an extra newline so let's delete it
    if text.find("\n", len(text)-1, len(text)) != -1:
      text = text[0:len(text)-1]

    self.app.save_hour(text, self.curr_rating, self.selected_tags)
    self.update_hour()

    # TODO: save location
    # print(w.window.current_location())
    

  def update_tags(self, item, id):
    tags = self.app.get_tags()
    attached_tags = self.app.get_item_tags(item, id)

    self.selected_tags = []
    for tag in tags:
      if(tag['id'] in attached_tags):
        text_color = self.tag_selected_text_color
        bg_color = self.tag_selected_background_color
        self.selected_tags.append(tag['id'])
      else:
        text_color = self.tag_text_color
        bg_color = self.tag_background_color
      
      self.window["select_tag" + str(tag['id'])].Update(value=tag['name'], text_color=text_color, background_color=bg_color)
      self.window["hash_tag" + str(tag['id'])].Update(background_color=bg_color)
      self.window["edit_tag" + str(tag['id'])].Update(value=tag['name'])


  def select_tag(self, tag_label):
    tag_ar = tag_label.split("_tag")
    tag_id = int(tag_ar[1])
    if tag_id not in self.selected_tags:
      self.selected_tags.append(tag_id)
    else:
      self.selected_tags.remove(tag_id)


  def start_edit_tags(self):
    self.window['tags_click'].Update(visible=False)
    self.window['tags_edit'].Update(visible=True)
    self.edit_tags = True


  def cancel_edit_tags(self):
    self.window['tags_edit'].Update(visible=False)
    self.window['tags_click'].Update(visible=True)
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

  reset_db("data.db")

  w = PreciousWindow()

  # Event Loop to process "events" and get the "values" of the inputs
  while True:
    event, values = w.window.read()
    if event in (None, 'Cancel'):   # if user closes window or clicks cancel
      break

    # hour text saving: happens after space/return or dot typing
    elif event == "hour_text":
      w.save(values)

    # click on the current hour in the list -- reload it
    elif event == 'hour_current':
      w.change_hour(event, 0)

    # load the current system date hour
    elif event == 'now':
      w.current_hour()      

    # change hour rating
    elif event == "bad":
      w.update_rating(-1)
      w.save(values)
    elif event == "neutral":
      w.update_rating(0)
      w.save(values)
    elif event == "good":
      w.update_rating(1)
      w.save(values)      

    # navigate hours using hour buttons
    elif event.find("hour_dec_") != -1:
      w.save(values)
      w.change_hour(event, (-1) * int(event.replace("hour_dec_","")))
    elif event.find("hour_inc_") != -1:
      w.save(values)
      w.change_hour(event, int(event.replace("hour_inc_","")))

    # navigate hours using arrows
    elif event == 'prev':
      w.save(values)
      w.change_hour(event, -1)
    elif event == 'next':
      w.save(values)
      w.change_hour(event, +1)

    # open/close menu
    elif event == "menu":
      w.menu_visible = not w.menu_visible
      w.window['menu_column'].Update(visible=w.menu_visible)

    # start editing tags
    elif event == "edit_tags":
      if w.edit_tags:
        w.cancel_edit_tags()
      else:
        w.start_edit_tags()

    # stop editing tags (when pressed cancel in the editing mode)
    elif event == "cancel_edit_tags":
      w.cancel_edit_tags()

    # save tags and stop editing tags
    elif event == "save_tags":
      print('TODO: save tags')
      w.cancel_edit_tags()

    # select tag
    elif event.find("select_tag") != -1 or event.find("hash_tag") != -1:
      w.select_tag(event)
      w.save(values)

    # open plot window
    elif event == "plot":
      layout2 = [
        [sg.Text('Plot window', background_color=sg.theme_background_color())],
        [sg.Canvas(size=(400, 300), key='canvas')],
        [sg.Button('Exit')]
      ]
      # TODO: create proper window, plot stuff
      # TODO: also -- probably need to keep both windows opened and working? -- see docs on how to
      w.window.Hide()
      win2 = sg.Window('Plot window', layout2)
      while True:
          ev2, vals2 = win2.read()
          if ev2 is None or ev2 == 'Exit':
              win2.close()
              break

      w.window.UnHide()

    else:
      print("Unknown event")
      print(event)
      print(values)

    # print('You entered ', values[0])
    # print(values)

  w.window.close()