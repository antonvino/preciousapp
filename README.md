# Precious App
Time is precious, so log what you did every hour, use tags. Later you can view a plot of your progress and see some very nice insights about your productivity patterns.

It has been proven that reviewing your days helps you increase productivity and improves your mood because you feel more in control and see tangible improvements of your life and personality. Logging your hours helps you value every hour while catching yourself on how you get lazy or procrastinate. This app is a simple tool that can do wonders.

# Screenshots
![](screenshots/latest.png)

# How to launch
```python3 precious.py```

# PySimpleGUI
This library is used to create the GUI of the app

All docs are here https://pysimplegui.readthedocs.io/en/latest/

# Requirements
As per PySimpleGUi docs for development need to install tkinter

```apt-get install tkinter```

AND

```pip install pysimplegui```

or (usually needed on linux)

```pip3 install pysimplegui```

sqlite (in Python) is used for database management and should be installed in your Python


# TODO

## For first release:

- [ ] Autosave hour all the time, on every click or even with timer (autosave) — that’s how notes do it
- [x] Textarea adds \n on every save, remove the last \n from text…
- [x] Status text should be on the left bottom
- [x] Click on “up” should move one hour up, same with “down” — hour down
- [ ] Ctrl+arrow up/down should do the same as arrow up/down buttons in GUI
- [x] “Now” button should show current hour from the system
- [ ] “Plot” button should open the window with a canvas ready for plotting
- [ ] “Day”  button should load the day logging — text area should the day, label shows day, save button has “save day”, cancel button should say “back to hours” which leads to the current hour of the chosen day. List of hours should show days in the day mode. Now button should be “today”. “Day” button should become “Hour”.     Another, simpler, option would be to open a separate window with the same layout and just arrows for days but it may make things cumbersome.
- [x] Saving hour should not remove # from tags, need to add # in update_tags function
- [x] Hour text should be empty if hour has not been saved yet
- [ ] Ctrl+Enter should save hour/day, Ctrl+S should do the same
- [ ] Button up from 5AM should offer to go to Previous day which rolls hours so that 5AM is at the bottom. Below 12AM should offer to go to Next day which rolls hours so that 1AM is at the top
- [x] Default tags should be: “work”, “self-development”, “sport”, “family”, “friends”
- [x] Design the colours fully for dark mode, use green colours from the logo — nice to keep the theme going
- [ ] How to make a perma-app in sidebar on Linux/Mac/Windows -- Work it out, release the app.


## Features:

- [ ] Tags edit function should be less hidden - it's hard to guess it's on right click and tooltip is no good
- [ ] Tags editing should happen in their select window, it should just change into textarea with tags. Or if that’s not possible — edit in a separate window.
- [ ] Settings: save last window position (every save of hour also saves last window positions) and open app window where it was last opened
- [ ] Design the colours fully for light mode, use green colours from the logo — nice to keep the theme going
- [ ] Settings: dark mode / light mode
- [ ] Encryption: encrypt when saving, decrypt when showing. Do with dummy auto password as first to test
- [ ] Settings: need to set up password for encryption and switch encryption on/off
- [ ] Settings: Choose between 24hr OR PM/AM mode
- [ ] Settings: Autosaving on/off
- [ ] Settings: Show tip of the day on launch on/off
- [ ] Tip of the day: a separate little window with a tip, would be cool to draw isometric art for this i.e. “look at yourself from a 3rd person view — person at a phone sitting with a health bar?” Create a few tips and show them at random. Tips are shown at launch of the setting is not off (default: on)
- [ ] Add tooltips (pysimplegui supports that so why not)
- [ ] Plotting of data
