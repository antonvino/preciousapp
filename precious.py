#!/usr/bin/python3

import PySimpleGUI as sg
from app import PreciousApp

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

"""

pa = PreciousApp()

# sg.theme('LightGrey1')
# sg.theme('NeutralBlue')
sg.theme('DarkBlue14')

sg.theme_text_color('#c0c0c0')
cols = sg.theme_button_color()
sg.theme_button_color(tuple(['#c0c0c0', cols[1]]))
sg.theme_element_text_color('#c0c0c0')
sg.theme_input_text_color('#c0c0c0')

print(sg.theme_slider_border_width())

column1 = [
            [sg.Listbox(values=(' 1 PM', ' 2 PM', ' 3 PM', ' 4 PM', ' 5 PM', ' 6 PM', ' 7 PM', ' 8 PM', ' 9 PM', ' 10 PM', ' 11 PM'), size=(10, 10), enable_events=True, key="select_hour", background_color=sg.theme_background_color(), no_scrollbar=True)],#, sg.VerticalSeparator()],
]

column2 = [
            [
              # sg.Text('', size=(4,1)), 
              sg.Button('←', key="prev_hour", font="Roboto 12 normal", size=(4,1)), 
              sg.Button(pa.get_hour_label(), key="open_day", size=(18,1), pad=((65, 0), (0, 0)), button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0, font='Roboto 12 underline'), 
              sg.Button('→', key="next_hour", font="Roboto 12 normal", pad=((65, 0), (0, 0)), size=(4,1)),
              # sg.Text('', size=(4,1)), 
            ],
            [
              # sg.Slider( range=(1,3), default_value=2, size=(10,40), orientation='horizontal', resolution=1, font=('Roboto', 12), tick_interval=0, pad=((0,0), (0,0)), disable_number_display=True )
              sg.Button('Bad', key="bad", font="Roboto 10 normal",         size=(4,1), pad=((225, 0), (0, 0)),  border_width=1), 
              sg.Button('Neutral', key="neutral", font="Roboto 10 normal", size=(4,1), pad=((0, 0), (0, 0)),    border_width=0, button_color=("#444444", "#bbbbbb")), 
              sg.Button('Good', key="good", font="Roboto 10 normal",       size=(4,1), pad=((0, 0), (0, 0)))

            ],
            [
              sg.Multiline( default_text='Log the hour', size=(30, 6), key="hour_text", pad=((5, 0), (10, 0)), 
                            do_not_clear=True, focus=True, background_color=sg.theme_background_color() ),
              sg.Listbox(values=pa.get_tags(), 
                        size=(15, 6), enable_events=True, key="select_tag", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                        background_color=sg.theme_background_color(), pad=((5, 0), (10, 0)), no_scrollbar=False, 
                        right_click_menu = ['!Tags', ['!Tags', '&Edit tags::edit_tags']])
            ],
            [
              sg.Button('Save hour', key="save", font="Roboto 10 normal", size=(8,1), pad=((5, 0), (10, 0))), 
              sg.Text('', key="status", size=(24,1), pad=((10, 0), (10, 0))),
              sg.Button('View plot', key="open", font="Roboto 10 normal", size=(8,1), pad=((10, 0), (10, 0))), 
            ]
            #, sg.Button('Sun 26 Apr', key="open_day", button_color=('#000000', sg.theme_background_color()), border_width=0, font='Roboto 10 underline')]
]

# column3 = [
#             [sg.Listbox(values=(' my tag', ' my tag 2', ' appdev', ' work', ' hobby', ' climbing'), 
#                         size=(10, 12), enable_events=True, key="select_tag", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
#                         background_color=sg.theme_background_color(), pad=((5, 5), (5, 5)), no_scrollbar=True
#             )],
# ]

# All the stuff inside your window.g
layout = [ 
  [
    sg.Column(column1),
    sg.Column(column2),
    # sg.Column(column3)
  ]
  # [sg.Text('_' * 80)],
]

edit_tags = False

# Create the Window
window = sg.Window('Precious app', layout, font='Roboto 10 normal')

# Event Loop to process "events" and get the "values" of the inputs
while True:
  event, values = window.read()
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
    hour_label = window["open_day"] # this is the hour/day label
    pa.to_prev_hour()
    hour_label.Update(text=pa.get_hour_label())

  elif event == 'next_hour':
    hour_label = window["open_day"] # this is the hour/day label
    pa.to_next_hour()
    hour_label.Update(text=pa.get_hour_label())

  elif event == 'Edit tags::edit_tags':
    tags_listbox = window["select_tag"]
    tags_listbox.Update(disabled=True)

    hour_text = window["hour_text"]

    strval = ""
    for tag in pa.get_tags():
      strval += "#{0}, ".format(tag)

    strval += "#" # prompt new tag
    hour_text.Update(value=strval)

    save_button = window["save"]
    save_button.Update(text="Save tags")

    open_button = window["open"]
    open_button.Update(text="Cancel")

    edit_tags = True

  elif event == 'open':

    if edit_tags:
      tags_listbox = window["select_tag"]
      tags_listbox.Update(disabled=False)

      hour_text = window["hour_text"]
      hour_text.Update(value="Load hour data again")

      save_button = window["save"]
      save_button.Update(text="Save hour")

      open_button = window["open"]
      open_button.Update(text="View plot")

      edit_tags = False

    else:
      print("TODO: open plot")

  elif event == "save":

    tags = values['hour_text'].split(", #")
    valid_tags = []
    for tag in tags:
      tag = tag.replace("#", "").replace("\n","")
      if len(tag) > 0:
        valid_tags.append(tag) 
    
    print(valid_tags)
    pa.save_tags(valid_tags)

    tags_listbox = window["select_tag"]
    tags_listbox.Update(disabled=False)

    hour_text = window["hour_text"]
    hour_text.Update(value="Load hour data again")

    save_button = window["save"]
    save_button.Update(text="Save hour")

    open_button = window["open"]
    open_button.Update(text="View plot")

    tags_listbox = window["select_tag"]
    tags_listbox.Update(values=pa.get_tags())

    open_button = window["status"]
    open_button.Update(value="Tags saved.")

    edit_tags = False

  else:
    print(event)
    print(values)

  # print('You entered ', values[0])
  # print(values)

window.close()