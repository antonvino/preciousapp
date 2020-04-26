"""
Services for logs app
"""

def pack_json_data(days, hours, style = "week"):
    from logs.models import Day, Hour
    import datetime
    import json
    """
    Pack the days&hours data in JSON format for the chart representation
    That data will be passed onto d3 chart js
    :param days:
    :param hours:
    :param style:
    :return:
    """
    types = {0:'Bad', 1:'Neutral', 2:'Good'}
    
    json_data = []
    # each type is a dictionary of days
    for productive, key in types.items():
        day_dict = {'key': key, 'values': []}
        
        # each day is a dictionary of chart data
        for day in days:
            
            x_label = None
            hour_count = 0

            # count the hours
            for hour in hours:
                if (hour.day.id == day.id) and (hour.productive == productive):
                    hour_count += 1
            
            date = day.date
            if style == "week":
                # get weekday
                x_label = date.strftime("%a")

            elif style == "month":
                x_label = date.day
                
            elif style == "overall":
                x_label = '%d/%d' % (date.day, date.month,)
            
            # set the chart values for this day
            day_dict['values'].append({'x': x_label, 'y': hour_count})
        
        json_data.append(day_dict)
                
    json_data = json.dumps(json_data)
    
    return json_data
    

def calc_stats(days, hours):
    from logs.models import Day, Hour
    import math
    """
    Calculate stats based on the given loaded data for days/hours
    :param days:
    :param hours:
    :return: set of stats
    """
    total_hours = days.count() * 24
    logged_hours = hours.count()
    if logged_hours > 0:
        bad_hours = hours.filter(productive = 0).count()
        neutral_hours = hours.filter(productive = 1).count()
        good_hours = hours.filter(productive = 2).count()
        # FORMULA: 100*(good/(logged - neutral))
        if neutral_hours != logged_hours:
            efficiency = '%d' % math.floor((float(good_hours)/(float(logged_hours)-float(neutral_hours)))*100)
            efficiency += '%'
        else:
            efficiency = 'N/A'
    else:
        logged_hours = 'N/A'
        bad_hours = 'N/A'
        neutral_hours = 'N/A'
        good_hours = 'N/A'
        efficiency = 'N/A'
    return total_hours, logged_hours, bad_hours, neutral_hours, good_hours, efficiency


def extract_tags(text):
    """
    Extract hashtags from given text and return a set
    :param text:
    :return: set of tags
    """
    import re
    return [re.sub(r"(\W+)$", "", j) for j in set([i[1:] for i in text.split() if i.startswith("#")])]

