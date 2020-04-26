#!/usr/bin/python3

import PySimpleGUI as sg
from data import PreciousData
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

sg.theme('LightGreen2')   # Add a touch of color

column1 = [
            [sg.Listbox(values=(' 1 PM', ' 2 PM', ' 3 PM', ' 4 PM', ' 5 PM', ' 6 PM', ' 7 PM', ' 8 PM', ' 9 PM', ' 10 PM', ' 11 PM'), size=(10, 10), enable_events=True, key="select_hour", background_color=sg.theme_background_color(), no_scrollbar=True)],#, sg.VerticalSeparator()],
]

column2 = [
            [
              # sg.Text('', size=(4,1)), 
              sg.Button('←', key="prev_hour", font="Roboto 12 normal", size=(4,1)), 
              sg.Button('{0}'.format(pa.get_hour_label(pa.get_current_time())), key="open_day", size=(18,1),     pad=((65, 0), (0, 0)), button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0, font='Roboto 12 underline'), 
              sg.Button('→', key="next_hour", font="Roboto 12 normal", pad=((65, 0), (0, 0)), size=(4,1)),
              # sg.Text('', size=(4,1)), 
            ],
            [
              sg.Multiline(default_text='Log the hour', size=(30, 6), key="hour_text", pad=((5, 0), (10, 0)), do_not_clear=False, focus=True), 
              sg.Listbox(values=(' my tag', ' my tag 2', ' appdev', ' work', ' hobby', ' climbing'), 
                        size=(15, 6), enable_events=True, key="select_tag", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                        background_color=sg.theme_background_color(), pad=((5, 0), (10, 0)), no_scrollbar=False, 
                        right_click_menu = ['!Tags', ['!Tags', '&Edit tags']])
            ],
            [
              sg.Button('Save hour', key="save_hour", font="Roboto 10 normal", size=(8,1), pad=((5, 0), (10, 0))), 
              sg.Text('Error text', text_color='Red', size=(24,1), pad=((10, 0), (10, 0))),
              sg.Button('View plot', key="open_plot", font="Roboto 10 normal", size=(8,1), pad=((10, 0), (10, 0))), 
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

# Create the Window
window = sg.Window('Precious app', layout, font='Roboto 10')
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

  else:
    print(event)
    print(values)

  # print('You entered ', values[0])
  # print(values)

window.close()