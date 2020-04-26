"""
Main app controller file
Uses PyObjC wrappers
Uses Requests (communicates with a Django web app)

Author:
The original author of the Precious app is Anton Vinokurov (www.antonvino.com)
"""

from Cocoa import *
from Foundation import NSObject
import json, os, signal, time
from datetime import datetime, timedelta, date

# Precious Web site URL
SITE_URL = 'http://mytimeisprecious.com/'
#SITE_URL = 'http://127.0.0.1:8000/'

class PreciousUser():

    def __init__(self):
        self.token = None

    def authenticate(self, email, password):
        print 'authenticating...'
        import requests

        # construct auth data using the fields
        auth_data = {
            'username': email,
            'password': password
        }

        # get token for the user
        url = SITE_URL + 'api/token-auth/'
        print url
        print auth_data
        r = requests.post(url, data=auth_data)
        response = r.json()
        if 'token' in response:
            self.token = response['token']
            self.email = auth_data['username']
        else:
            print '[Auth error] {0}'.format(r.text)
            error = 'E-mail or password do not match.'
            if 'non_field_errors' in response:
                error = response['non_field_errors'][0]
            raise ValueError(error)

    def create(self, email, username, password):
        print 'creating an account...'
        import requests

        # construct auth data using the fields
        auth_data = {
            'email': email,
            'username': username,
            'password': password
        }

        # get token for the user
        url = SITE_URL + 'api/sign-up/'
        print url
        print auth_data
        r = requests.post(url, data=auth_data)
        print r.text

        response = r.json()
        if 'id' not in response:
            # Django sends errors for each field
            if 'email' not in response:
                response['email'] = ['']
            if 'username' not in response:
                response['username'] = ['']
            raise ValueError(response['email'][0], response['username'][0])

        self.email = response['email']
        # token = r.json()
        # if 'token' in token:
        #     self.token = token['token']
        #     self.email = auth_data['username']


class PreciousData():

    def __init__(self):
        pass

    def load(self, year = None, month = None, day = None, hour = None):
        """
        Loads the data from JSON file according to given date

        :return: A tuple: reflection, activity, productive
        """

        # getting the system date and time if they are not set
        if not year or not month or not day or (not hour and hour != 0):
            today = datetime.now()
            year = today.year
            month = today.month
            day = today.day
            hour = today.hour

        # convert date and hour to strings
        year = str(year)
        month = str(month)
        day = str(day)
        hour = str(hour)

        try:
            # open the file to read data from
            fr = open('precious_mytime.js', 'r')
            # load and decode the JSON data
            json_data = json.load(fr)
            # close the file
            fr.close
        except IOError:
            # file does not exist yet - set json_data to an empty dictionary
            print '[Data:Error] File not found'
            json_data = {}

        reflection = None
        activity = None
        productive = None
        if year in json_data and month in json_data[year] and day in json_data[year][month]:
            if 'reflection' in json_data[year][month][day]:
                reflection = json_data[year][month][day]['reflection']
            if hour in json_data[year][month][day]:
                activity = json_data[year][month][day][hour]['activity']
                productive = json_data[year][month][day][hour]['productive']

        return reflection, activity, productive

    # load last hour logged
    # def getLast(self):
    #     try:
    #         # open the file to read data from
    #         fr = open('precious_mytime.js', 'r')
    #         # load and decode the JSON data
    #         json_data = json.load(fr)
    #         # close the file
    #         fr.close
    #         # init datetime and time modules
    #         hour_inc = 0
    #         reflection = None
    #         # activity = None
    #         # run a loop to find the latest activity or reflection from before
    #         while hour_inc < 86400 and not reflection:
    #             # get the date and time from earlier
    #             today = datetime.fromtimestamp(time.time()-hour_inc) # this hour, last hour, 2 hours earlier etc.
    #             year = str(today.year)
    #             month = str(today.month)
    #             day = str(today.day)
    #             # hour = str(today.hour)
    #             # 1 hour earlier
    #             hour_inc += 3600
    #
    #             # try to access data by the loaded year-month-day-hour keys
    #             try:
    #                 # self.activity = json_data[year][month][day][hour]['activity']
    #                 reflection = json_data[year][month][day]['reflection']
    #             except KeyError:
    #                 print 'Previous hour not found'
    #             self.reflection = reflection
        #
        # except IOError:
        #     # file does not exist yet
        #     print 'File not found'

    def save(self, type, productive = 1, activity = None, reflection = None, year = None, month = None, day = None, hour = None):
        """
        Saves the data for Hour or Day in a JSON file

        :param type: `day` or `hour`
        :param productive: 1/2/3 as in low/med/high
        :param activity: text about activity
        :param reflection: reflection of the day

        other parameters are self-explanatory and should be numbers
        """

        # getting the system date and time if they are not set
        if not year or not month or not day or (not hour and hour != 0 and type != 'day'):
            today = datetime.now()
            year = today.year
            month = today.month
            day = today.day
            # hour = today.hour
            hour = int(today.strftime('%H')) # need a 24 hour

        # convert date and hour to strings
        year = str(year)
        month = str(month)
        day = str(day)
        hour = str(hour)

        try:
            # open the file to read data from
            fr = open('precious_mytime.js', 'r')
            # load and decode the JSON data
            json_data = json.load(fr)
            # close the file
            fr.close
        except IOError:
            # file does not exist yet - set json_data to an empty dictionary
            print '[Data:Error] Could not open the file precious_mytime.js'
            json_data = {}

        # this accounts for the problem when year/month/day have not been set yet in the JSON file
        if year not in json_data:
            json_data[year] = {};
        if month not in json_data[year]:
            json_data[year][month] = {}
        if day not in json_data[year][month]:
            json_data[year][month][day] = {}

        # logging hour
        if type == 'hour':
            # if this hour is not in the JSON file yet
            if hour not in json_data[year][month][day]:
                json_data[year][month][day][hour] = {}
            # append the hour data to the appropriate decoded node of the json_data
            json_data[year][month][day][hour].update({
                'productive': productive,
                'activity': activity
            })
        # logging day
        elif type == 'day':
            # append the hour data to the appropriate decoded node of the json_data
            json_data[year][month][day].update({
                'reflection': reflection
            })
        try:
            # open the file to rewrite data
            fw = open('precious_mytime.js', 'w')
            # JSON dump of the data
            json.dump(json_data, fw)
            print '[Data] {0} saved'.format(type)
            # close the file
            fw.close
        except IOError:
            print '[Data:Error] Could not open the file precious_mytime.js'

    def sync(self, all = False):
        """
        Syncs the data with Web API of Precious Web
        Loads data from local JSON file
        Saves data on the web
        Using Python Requests
        Requires user instance to be authenticated (i.e. to have a valid token)
        Syncs all data only if all=True, otherwise syncs last 3 days
        """

        assert(user.token is not None)

        import requests

        print '[Data] Syncing start...'
        # what has been synced
        word = 'All data'

        headers = {'Authorization': 'Token {0}'.format(user.token), 'user-agent': 'precious-app/1.0.0'}

        url = SITE_URL + 'api/users?email={0}'.format(user.email)
        print '[API] Authorized user {0}'.format(url)
        r = requests.get(url, headers=headers)
        users = r.json()
        print r.text
        user_data = users.pop()

        url = SITE_URL + 'api/users/{0}'.format(user_data['id'])
        print '[API] Authorized user detailed {0}'.format(url)
        r = requests.get(url, headers=headers)
        user_data = r.json()
        user.username = user_data['username']
        user.email = user_data['email']
        user.id = user_data['id']

        # check if the new version of the app
        # needs loading previous data from the server
        if precious_settings.is_new_version is True:
            self.back_sync()
            word = 'Old data'
        # otherwise proceed with the normal sync
        # TODO: not a very concise way of checking this
        else:
            # 3 days ago datetime
            dt = datetime.now() - timedelta(days=3)

            # request recently logged days
            url = SITE_URL + 'api/days?synced_after={0}&author={1}'.format(dt, user.id)
            r = requests.get(url, headers=headers)
            days = r.json()
            print '[API] {0}'.format(url)
            recent_days = []
            for day in days:
                recent_days.append(day['date'])
                # request recently logged hours data
                url = SITE_URL + 'api/hours?synced_after={0}&day={1}&author={2}'.format(dt, day['id'], user.id)
                r = requests.get(url, headers=headers)
                hours = r.json()
                print '[API] {0}'.format(url)
                recent_hours = []
                for hour in hours:
                    recent_hours.append('{0}-{1}'.format(day['date'],hour['hour']))
                # print repr(recent_hours)
            # print repr(recent_days)

            # open the file to read data from
            fr = open('precious_mytime.js', 'r')
            # load and decode the JSON data
            json_data = json.load(fr)

            # flag and arrays not to redo the already synced stuff
            # in case the connection breaks and the loop has to restart
            all_done = False
            days_done = []
            hours_done = []
            # we repeat this loop until all is done (this may take a while)
            # and frankly it may not be the most elegant way of doing it
            # but as it's a one off thing you'd do for full sync - it's not too bad
            # for 3 past days sync it won't be needed often
            while not all_done:
                try:
                    print 'Wait for 3 seconds...'
                    time.sleep(3)
                    for year in json_data:
                        for month in json_data[year]:
                            for day in json_data[year][month]:

                                day_date = date(day=int(day), month=int(month), year=int(year))

                                # we only sync the data, that is 3 days old or less
                                # if all==True - we sync all data
                                if all == True or day_date >= dt.date():
                                    # do this only if the day has not been synced in the previous loop
                                    if str(day_date) not in days_done:
                                        print '[API] Day POST/PUT'
                                        # construct the day data dict
                                        day_data = {'author':user.id, 'date':day_date}
                                        if 'reflection' in json_data[year][month][day]:
                                            day_data['day_text'] = json_data[year][month][day]['reflection']

                                        this_day = {}
                                        # if day has not been logged in the last 3 days - try to add a new one
                                        if str(day_date) not in recent_days:
                                            url = SITE_URL + 'api/days/'
                                            print '[API] POST {0}'.format(url)
                                            # POST new day
                                            r = requests.post(url, data=day_data, headers=headers)

                                        # otherwise update the existing one
                                        else:
                                            url = SITE_URL + 'api/days/?date={0}&author={1}'.format(day_date, user.id)
                                            print '[API] GET {0}'.format(url)
                                            r = requests.get(url, headers=headers)
                                            this_day = r.json()
                                            this_day = this_day.pop()
                                            # the PUT url
                                            url = SITE_URL + 'api/days/{0}/'.format(this_day['id'])
                                            print '[API] PUT {0}'.format(url)
                                            # PUT (update) the day
                                            r = requests.put(url, data=day_data, headers=headers)

                                        # Request result debug
                                        # print r.text

                                        # request day ID
                                        # TODO refactor into one function with above
                                        if 'id' not in this_day:
                                            url = SITE_URL + 'api/days/?date={0}&author={1}'.format(day_date, user.id)
                                            print '[API] GET {0}'.format(url)
                                            r = requests.get(url, headers=headers)
                                            this_day = r.json()
                                            this_day = this_day.pop()

                                        for hour in json_data[year][month][day]:

                                            if hour != 'reflection':

                                                print '[API] Hour POST/PUT'

                                                hour_data = {'author':user.id, 'day':this_day['id'], 'hour':hour}

                                                if 'activity' in json_data[year][month][day][hour]:
                                                    hour_data['hour_text'] = json_data[year][month][day][hour]['activity']
                                                if 'productive' in json_data[year][month][day][hour]:
                                                    hour_data['productive'] = json_data[year][month][day][hour]['productive']

                                                hour_date = '{0}-{1}'.format(day_date, hour)
                                                # do this only if hour has not been synced in the previous loop
                                                if hour_date not in hours_done:
                                                    # if hour has not been logged in the last 3 days - try to add a new one
                                                    if hour_date not in recent_hours:
                                                        url = SITE_URL + 'api/hours/'
                                                        print '[API] POST {0}'.format(url)
                                                        # POST new hour
                                                        r = requests.post(url, data=hour_data, headers=headers)

                                                    # otherwise update the existing one
                                                    else:
                                                        url = SITE_URL + 'api/hours/?day={0}&hour={1}&author={2}'.format(this_day['id'], hour, user.id)
                                                        print '[API] GET {0}'.format(url)
                                                        r = requests.get(url, headers=headers)
                                                        this_hour = r.json()
                                                        this_hour = this_hour.pop()
                                                        # the PUT url
                                                        url = SITE_URL + 'api/hours/{0}/'.format(this_hour['id'])
                                                        print '[API] PUT {0}'.format(url)
                                                        # PUT (update) the hour
                                                        r = requests.put(url, data=hour_data, headers=headers)

                                                    # Request result debug
                                                    # print r.text

                                                    # save the hour in hours done
                                                    hours_done.append(hour_date)

                                        # END FOR "for all hours"
                                        # save the day in days_done
                                        days_done.append(day_date)

                    # END FOR "for all days"
                    # close the file
                    fr.close
                    # set the flag - loop will not be entered anymore
                    all_done = True

                except Exception, e:
                    print '[API] Error in sync loop: {0}'.format(e)
            # END WHILE
        # END ELSE
        # return what has been synced
        if not all:
            word = 'Past 3 days'
        return word
        # except IOError:
        #     # file does not exist yet - set json_data to an empty dictionary
        #     print 'File not found'
        #     json_data = {}

    def back_sync(self):
        """
        Loads the data with Web API of Precious Web
        Saves the data in local JSON file
        Using Python Requests
        Requires user instance to be authenticated (i.e. to have a valid token)
        """
        assert(user.token is not None)
        assert(user.email is not None)

        import requests

        print '[Data] Syncing start...'

        headers = {'Authorization': 'Token {0}'.format(user.token), 'user-agent': 'precious-app/1.0.0'}

        # request all logged days
        url = SITE_URL + 'api/days?author={0}'.format(user.id)
        r = requests.get(url, headers=headers)
        days = r.json()
        if len(days) > 0:
            for day_data in days:
                day_date = datetime.strptime(day_data['date'], '%Y-%m-%d')
                year = day_date.year
                month = day_date.month
                day = day_date.day
                print 'day:{0}-{1}-{2}'.format(day, month, year)

                # log the day locally
                precious_data.save(
                type='day',
                reflection=day_data['day_text'],
                year=year,
                month=month,
                day=day)

                # for each day get hours
                url = SITE_URL + 'api/hours?author={0}&day={1}'.format(user.id, day_data['id'])
                r = requests.get(url, headers=headers)
                hours = r.json()
                for hour in hours:
                    # log the hour locally
                    precious_data.save(
                        type='hour',
                        productive=hour['productive'],
                        activity=hour['hour_text'],
                        year=year,
                        month=month,
                        day=day,
                        hour=hour['hour'])

        # if everything went successfully
        precious_settings.is_new_version = False
        precious_settings.save()


class PreciousSettings():

    def __init__(self):
        pass

    def load(self):
        """
        Loads the settings data from a JSON file
        """
        # getting the system date and time if they are not set
        try:
            # open the file to read data from
            fr = open('precious_mysettings.js', 'r')
            # load and decode the JSON data
            json_data = json.load(fr)

            # is it a new app version?
            self.is_new_version = bool(json_data['is_new_version'])
            # activate app each hour or not?
            self.activate_each_hour = bool(json_data['activate_each_hour'])

            print '[Data] Settings loaded'

            # close the file
            fr.close
        except IOError:
            # file does not exist yet - set json_data to an empty dictionary
            print '[Data:Error] Could not open the file precious_mysettings.js'
            #json_data = {}

    def save(self):
        """
        Saves the settings data into a JSON file
        """
        json_data = {
            'is_new_version': int(self.is_new_version),
            'activate_each_hour': int(self.activate_each_hour),
        }
        try:
            # open the file to rewrite data
            fw = open('precious_mysettings.js', 'w')
            # JSON dump of the data
            json.dump(json_data, fw)
            print '[Data] Settings saved'
            # close the file
            fw.close
        except IOError:
            print '[Data:Error] Could not open the file precious_mysettings.js'


class PreciousController(NSWindowController):
    # Hour window
    hourLabel = objc.IBOutlet()
    hourField = objc.IBOutlet()
    hourButton = objc.IBOutlet()
    hourProgress = objc.IBOutlet()
    hourSegment = objc.IBOutlet()

    # Day window
    dayLabel = objc.IBOutlet()
    dayField = objc.IBOutlet()
    dayButton = objc.IBOutlet()
    dayProgress = objc.IBOutlet()

    # Sign up window
    signUpWindow = objc.IBOutlet()
    signUpEmailField = objc.IBOutlet()
    signUpUsernameField = objc.IBOutlet()
    signUpPasswordField = objc.IBOutlet()
    signUpProgress = objc.IBOutlet()
    signUpButton = objc.IBOutlet()
    signUpEmailError = objc.IBOutlet()
    signUpUsernameError = objc.IBOutlet()
    signUpError = objc.IBOutlet()

    # sync window
    syncWindow = objc.IBOutlet()
    usernameField = objc.IBOutlet()
    passwordField = objc.IBOutlet()
    syncProgress = objc.IBOutlet()
    syncButton = objc.IBOutlet()
    syncError = objc.IBOutlet()
    statsButton = objc.IBOutlet()

    # Miscellaneous items
    helpText = objc.IBOutlet()
    settMenuActivate = objc.IBOutlet()

    def windowDidLoad(self):
        """
        Initializing the main window controller
        Setting default field values and resetting everything
        """

        NSWindowController.windowDidLoad(self)
        # default data values in the window
        self.productive = 1
        self.activity = None
        self.reflection = None
        self.syncAllFlag = False

        # attempt to load current day/hour data
        self.loadData()
        # init the badge
        self.badge = NSApp.dockTile() 
        # stop animation of the progress indicators to hide them
        self.hourProgress.stopAnimation_(self)
        self.dayProgress.stopAnimation_(self)
        
        # set current datetime object and current timestamp
        self.curr_timestamp = time.time()
        self.reloadTime()
        
        # update displayed hour
        self.updateDisplayHour()
        self.updateDisplayDay()

        # init the help text
        self.setHelpText()

        # set the timer
        self.pending = 0
        self.pending_hours = []
        self.setPyTimer()

        # User PREFERENCES / SETTINGS
        precious_settings.load()
        # update settings states in the menu
        self.settMenuActivate.setState_(precious_settings.activate_each_hour)
        # check if it's the new version of the app
        if precious_settings.is_new_version is True:
            # bring sync window up
            self.requireSync()

    def requireSync(self):
        """
        Brings sync window up and asks to re-sync
        It's a cap until the re-sync is done
        """
        self.syncWindow.makeKeyAndOrderFront_(self)
        self.syncError.setStringValue_('Please log in to re-sync old data')
        self.syncError.setHidden_(False)
        self.syncAllFlag = True

    def setHelpText(self):
        """
        Reads help text from a faq.txt local file and puts it in the help form
        TODO: Webview of the HTML page instead?
        """
        try:
            # open the file to read data
            fw = open('faq.txt', 'r')
            # update help text
            self.helpText.setStringValue_(fw.read())
            # close the file
            fw.close
        except IOError:
            print '[File] File faq.txt was not found.'
    
    def reloadTime(self):
        """
        Takes current timestamp and updates the date/time data
        """
        self.curr_time = datetime.fromtimestamp(self.curr_timestamp)
        self.year = self.curr_time.year
        self.month = self.curr_time.month
        self.day = self.curr_time.day
        self.hour = int(self.curr_time.strftime('%H')) # need a 24 hour        

    def updateDisplayHour(self):
        """
        Updates the displayed date & hour in the interface
        """
        self.hourLabel.setStringValue_(self.curr_time.strftime('%a %d %b, %I %p'))
        self.dayLabel.setStringValue_(self.curr_time.strftime('%a %d %b'))
        self.dayButton.setStringValue_(self.curr_time.strftime('%a %d %b'))
        if self.activity:
            self.hourField.setStringValue_(self.activity)
            self.hourLabel.setTextColor_(NSColor.blackColor())
        else:
            self.hourField.setStringValue_('')
            # if not self.productive and self.productive != 0:
            self.hourLabel.setTextColor_(NSColor.redColor())
        if self.productive or self.productive == 0:
            self.hourSegment.setSelected_forSegment_(1, self.productive)
        else:
            self.hourSegment.setSelected_forSegment_(1, 1)

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

    def clearData(self):
        """
        Sets default data for Day & Hour fields
        """
        self.activity = None
        self.reflection = None
        self.productive = 1

    def loadData(self, year = None, month = None, day = None, hour = None):
        """
        Loads data for Day & Hour fields
        """
        self.reflection, self.activity, self.productive = precious_data.load(year, month, day, hour)

    ####
    # Timed things

    def endOfHour(self):
        print '[Timer] Timer routine called'
        self.setPyTimer()  # reset the timer

        now = datetime.now()
        if(now.minute == 59):
            print '[Timer] End of hour'

            # if activate each hour is On - bring the app to attention
            if precious_settings.activate_each_hour is True:
                # Bring app to top
                NSApp.activateIgnoringOtherApps_(True)

            # is this hour logged?
            reflection, activity, productive = precious_data.load(year = now.year, month = now.month, day = now.day, hour = now.hour)
            pending_hour = '{0}-{1}-{2}-{3}'.format(now.year, now.month, now.day, now.hour)
            # if not - add it to pending hours and increase the amount of pending hours
            if productive is None and pending_hour not in self.pending_hours:
                print '[Timer] Increase pending hours'
                self.pending += 1
                self.pending_hours.append(pending_hour)

        # if there are pending hours - update the badge
        if self.pending > 0:
            # Set badge icon to the current hour
            self.badge.setBadgeLabel_(str(self.pending))
        else:
            self.badge.setBadgeLabel_(None)
            # nc = NSNotificationCenter.defaultCenter()
            # nc.postNotificationName_object_userInfo_('love_note', None, {'path':'xyz'})

    def setPyTimer(self):
        from threading import Timer
        # today = datetime.now() HERE WE NEED TO SET TIMER FOR APPROPRIATE TIME!
        Timer(30, self.endOfHour, ()).start()  # 60 second timer

    ####
    # Interface elements actions

    @objc.IBAction
    def productive_(self, sender):
        """
        Operates the SelectedSegment choice of how productive the hour has been
        """
        self.productive = sender.selectedSegment()

    @objc.IBAction
    def prevHour_(self, sender):
        """
        Loads the previous hour data in the hour window
        """
        # decrement time
        self.curr_timestamp -= 3600
        self.switchDate()
        print '[Action] prev hour'

    @objc.IBAction
    def nextHour_(self, sender):
        """
        Loads the next hour data in the hour window
        """
        # increment the time
        self.curr_timestamp += 3600
        self.switchDate()
        print '[Action] next hour'

    @objc.IBAction
    def prevDay_(self, sender):
        """
        Loads the previous day data in the day window
        """
        # decrement the time
        self.curr_timestamp -= 86400
        self.switchDate()
        print '[Action] prev day'

    @objc.IBAction
    def nextDay_(self, sender):
        """
        Loads the next day data in the day window
        """
        # increment the time
        self.curr_timestamp += 86400
        self.switchDate()
        print '[Action] next day'

    # submit the data
    @objc.IBAction
    def submitHour_(self, sender):
        """
        Submits the hour log
        Removes the app icon badge
        Makes the hour label black
        Starts and stops the spinny thing
        """
        # check if it's the new version of the app
        if precious_settings.is_new_version is True:
            # bring sync window up
            self.requireSync()

        # start the progress spin
        self.hourProgress.startAnimation_(self)
        
        # getting the text from text fields
        self.activity = self.hourField.stringValue()
        # self.reflection = self.dayField.stringValue()

        # log the hour
        precious_data.save(
            type='hour',
            productive=self.productive,
            activity=self.activity,
            year=self.curr_time.year,
            month=self.curr_time.month,
            day=self.curr_time.day,
            hour=self.curr_time.hour)
        
        # set the hour label colour to black
        self.hourLabel.setTextColor_(NSColor.blackColor())

        # go for the next hour
        # self.curr_timestamp += 3600
        # self.switchHour()

        if '{0}-{1}-{2}-{3}'.format(self.curr_time.year,
                                    self.curr_time.month,
                                    self.curr_time.day,
                                    self.curr_time.hour) in self.pending_hours:
            print '[Timer] Decrease pending hours'
            self.pending -= 1
            if self.pending > 0:
                label = str(self.pending)
            else:
                label = None
            # update the badge
            self.badge.setBadgeLabel_(label)

        # stop the progress spin
        self.hourProgress.stopAnimation_(self)

    # submit the data
    @objc.IBAction
    def submitDay_(self, sender):
        """
        Submits the day log
        Makes the day label black
        Starts and stops the spinny thing
        """
        # check if it's the new version of the app
        if precious_settings.is_new_version is True:
            # bring sync window up
            self.requireSync()

        # start the progress spin
        self.dayProgress.startAnimation_(self)
        # getting the text from text field
        self.reflection = self.dayField.stringValue()
        
        precious_data.save(
            type='day',
            reflection=self.reflection,
            year=self.curr_time.year,
            month=self.curr_time.month,
            day=self.curr_time.day)
        
        # set the day label colour to black
        self.dayLabel.setTextColor_(NSColor.blackColor())
        # stop the progress spin
        self.dayProgress.stopAnimation_(self)

    @objc.IBAction
    def authenticate_(self, sender):
        """
        Authenticates user
        Syncs the Hour & Day data with the web API if authenticated
        Shows errors or success message
        Starts and stops the spinny thing
        """

        # play intro sound
        # sound = NSSound.soundNamed_('Frog')
        # sound.play()
        # start the spin
        self.syncProgress.startAnimation_(self)
        # hide the stats and result
        self.syncError.setHidden_(True)
        # self.statsButton.setEnabled_(False)
        self.statsButton.setHidden_(True)

        email = self.usernameField.stringValue()
        password = self.passwordField.stringValue()

        auth_success = False
        # print email
        try:
            user.authenticate(
                email=email,
                password=password)
            auth_success = True

        except ValueError, e:
            print '[Action:Error] Halt auth flow'
            print e
            self.syncError.setTextColor_(NSColor.redColor())
            self.syncError.setStringValue_(str(e))
            self.syncError.setHidden_(False)
            # stop the spin
            self.syncProgress.stopAnimation_(self)

        # if authenticated - sync data
        if user.token is not None and auth_success:
            word = precious_data.sync(all=self.syncAllFlag)
            try:
                # precious_data.sync()
                # success!
                self.syncError.setTextColor_(NSColor.blackColor())
                self.syncError.setStringValue_('{0} synced.'.format(word))
                self.syncError.setHidden_(False)
                # play success sound
                sound = NSSound.soundNamed_('Pop')
                sound.play()
                # self.statsButton.setEnabled_(True)
                self.statsButton.setHidden_(False)
                # stop the spin
                self.syncProgress.stopAnimation_(self)
                # clear the syncAll flag if it was set
                if self.syncAllFlag is True:
                    self.switchDate()  # also update the display
                    self.syncAllFlag = False

            except Exception, e:
                print '[Action:Error] Could not sync: {0}'.format(e)
                self.syncError.setTextColor_(NSColor.redColor())
                self.syncError.setStringValue_('Could not sync.')
                self.syncError.setHidden_(False)
                # stop the spin
                self.syncProgress.stopAnimation_(self)

    @objc.IBAction
    def signUp_(self, sender):
        """
        Registers user
        Shows errors or success message
        Starts and stops the spinny thing
        Opens the sync window on success
        """

        # start the spin
        self.signUpProgress.startAnimation_(self)

        email = self.signUpEmailField.stringValue()
        username = self.signUpUsernameField.stringValue()
        password = self.signUpPasswordField.stringValue()

        self.signUpEmailError.setHidden_(True)
        self.signUpUsernameError.setHidden_(True)
        self.signUpError.setHidden_(True)

        print email
        try:
            user.create(
                email=email,
                username=username,
                password=password
            )
            # auth after
            # self.user.authenticate(
            #     email=email,
            #     password=password
            # )
            # self.user.email = email
            # self.user.password = password

            # stop the spin
            self.signUpProgress.stopAnimation_(self)
            # tell that user needs to confirm his e-mail
            print '[Action] User registered'
            self.signUpError.setStringValue_('Done! A confirmation request has been sent to your e-mail.')
            self.signUpError.setTextColor_(NSColor.blackColor())
            self.signUpError.setHidden_(False)
            # minimize the window and show login
            # self.signUpWindow.close()
            self.syncWindow.makeKeyAndOrderFront_(self)
            # fill in the email field
            self.usernameField.setStringValue_(email)
            # self.passwordField.setStringValue(password)

        except ValueError, e:
            print e
            # email error
            if e[0]:
                # self.signUpEmailField.setTextColor_(NSColor.redColor())
                self.signUpEmailError.setStringValue_(str(e[0]))
                self.signUpEmailError.setHidden_(False)
            # username error
            if e[1]:
                # self.signUpUsernameField.setTextColor_(NSColor.redColor())
                self.signUpUsernameError.setStringValue_(str(e[1]))
                self.signUpUsernameError.setHidden_(False)
            # general error conclusion
            print '[Action:Error] Could not create a new account.'
            self.signUpError.setStringValue_('Could not create an account.')
            self.signUpError.setTextColor_(NSColor.redColor())
            self.signUpError.setHidden_(False)
            # stop the spin
            self.signUpProgress.stopAnimation_(self)

    @objc.IBAction
    def syncAll_(self, sender):
        self.syncAllFlag = True
        self.syncWindow.makeKeyAndOrderFront_(self)

    ####
    # Settings

    @objc.IBAction
    def settActivate_(self, sender):
        """
        Changes setting activate each hour
        """
        precious_settings.activate_each_hour = not precious_settings.activate_each_hour
        precious_settings.save()
        self.settMenuActivate.setState_(precious_settings.activate_each_hour)

    ####
    # Links

    @objc.IBAction
    def openStats_(self, sender):
        """
        Opens stats web page in a browser
        Assumes the user is logged in on the web app
        """
        print '[WEB] Opening stats...'
        sharedWorkspace = NSWorkspace.sharedWorkspace()
        sharedWorkspace.openURL_(NSURL.URLWithString_(SITE_URL))

    @objc.IBAction
    def openWebApp_(self, sender):
        """
        Opens precious_web app main page
        """
        print '[WEB] Opening web app...'
        sharedWorkspace = NSWorkspace.sharedWorkspace()
        sharedWorkspace.openURL_(NSURL.URLWithString_('http://www.antonvino.com/precious/'))

    @objc.IBAction
    def openPasswordReset_(self, sender):
        """
        Opens reset password page in web app
        Called when user forgot password from the login window
        """
        print '[WEB] Opening web app password reset...'
        sharedWorkspace = NSWorkspace.sharedWorkspace()
        sharedWorkspace.openURL_(NSURL.URLWithString_(SITE_URL + 'accounts/password-reset/'))

    @objc.IBAction
    def openPortfolio_(self, sender):
        """
        Opens author's portfolio in a browser
        """
        print '[WEB] Opening portfolio...'
        sharedWorkspace = NSWorkspace.sharedWorkspace()
        sharedWorkspace.openURL_(NSURL.URLWithString_('http://www.antonvino.com'))

if __name__ == "__main__":

    app = NSApplication.sharedApplication()
    
    # Initiate the controller with a XIB
    viewController = PreciousController.alloc().initWithWindowNibName_("Precious")

    user = PreciousUser()
    precious_data = PreciousData()
    precious_settings = PreciousSettings()

    # Show the window
    viewController.showWindow_(viewController)
    # viewController.badge = app.dockTile()
    # viewController.badge.setBadgeLabel_('1')

    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)        

    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()            