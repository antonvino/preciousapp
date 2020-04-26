from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, redirect
from logs.models import Day, Hour, User
import datetime
import json
from django.conf import settings

def sync_mac(request):
    """ 
    Syncs the hour/day data from the json sent by the precious_mac
    """
    #
    # TODO: in production need to have get_or_create not 
    # to update the pub_date
    # try:
    #     # open the file to read data from
    #     fr = open(settings.BASE_DIR + '/static/json/precious_mytime.js', 'r')
    #     # load and decode the JSON data
    #     json_data = json.load(fr)
    #     # close the file
    #     fr.close
    # except IOError:
    #     # file does not exist yet - set json_data to an empty dictionary
    #     print 'File not found'
    #     json_data = {}
    print 'sync sync sync'
    # print request.POST['data'];
    # for year, json_year in json_data.items():
    #     for month, json_month in json_year.items():
    #         for day, json_day in json_month.items():
    #
    #             reflection = None
    #             if 'reflection' in json_day:
    #                 reflection = json_day['reflection']
    #
    #             new_day, created = Day.objects.get_or_create(
    #                 year = year,
    #                 month = month,
    #                 day = day,
    #                 day_text = reflection
    #             )
    #             print new_day.day
    #
    #             for hour, json_hour in json_day.items():
    #                 activity = None
    #                 productive = None
    #
    #                 if hour != 'reflection':
    #                     if 'activity' in json_hour:
    #                         activity = json_hour['activity']
    #                     if 'productive' in json_hour:
    #                         productive = json_hour['productive']
    #
    #                     new_hour, created = Hour.objects.get_or_create(
    #                         day = new_day,
    #                         hour = hour,
    #                         productive = productive,
    #                         hour_text = activity
    #                     )
    #                     print new_hour.hour_text

    # return redirect(reverse("week-current"))
    return render(request, 'sync.html')
        

def sync_json(request):
    """ Syncs the hour/day data from the static JSON file
        TEMPORARY
    """
    #
    # TODO: in production need to have get_or_create not 
    # to update the pub_date
    try:
        # open the file to read data from
        fr = open(settings.BASE_DIR + '/static/json/precious_mytime.js', 'r')
        # load and decode the JSON data
        json_data = json.load(fr)
        # close the file
        fr.close
    except IOError:
        # file does not exist yet - set json_data to an empty dictionary
        print 'File not found'
        json_data = {}

    user = User.objects.order_by('created_at').first()
    print user

    for year, json_year in json_data.items():
        for month, json_month in json_year.items():
            for day, json_day in json_month.items():

                reflection = None
                if 'reflection' in json_day:
                    reflection = json_day['reflection']

                new_day, created = Day.objects.get_or_create(
                    datetime.date(year=year, month=month, day=day),
                    day_text=reflection,
                    author=user,
                )
                print new_day.day

                for hour, json_hour in json_day.items():
                    activity = None
                    productive = None
                    
                    if hour != 'reflection':
                        if 'activity' in json_hour:
                            activity = json_hour['activity']
                        if 'productive' in json_hour:
                            productive = json_hour['productive']

                        new_hour, created = Hour.objects.get_or_create(
                            day=new_day,
                            hour=hour,
                            productive=productive,
                            hour_text=activity,
                            author=user,
                        )
                        print new_hour.hour_text

    return redirect(reverse("week-current"))
