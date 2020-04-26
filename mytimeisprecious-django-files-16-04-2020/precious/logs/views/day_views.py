from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from logs.models import Day, Hour
from logs.services.logs_util import pack_json_data, calc_stats
from logs.forms.filter_forms import TagsFilterForm
from logs.templatetags.filter_tags import get_tags_path
from django.views.decorators.http import require_http_methods
import datetime


@login_required
def week_current(request):
    """ The summary of days this week 
        A basic view of all the logged hours as productivity stats
        The default view in future for the homepage
    """
    today = datetime.datetime.now()
    curr_date = '%d-%d-%d' % (today.day, today.month, today.year)    
    return week_by_date(request, curr_date)


@login_required
def week_by_date(request, week_date):
    """ The summary of days from the week defined by the date 
        A basic view of all the logged hours as productivity stats
    """
    week_date = week_date.split('-')  # Date format: DD-MM-YYYY
    given_date = datetime.date(
        day=int(week_date[0]), 
        month=int(week_date[1]), 
        year=int(week_date[2])
    )
    mon = given_date - datetime.timedelta(days=given_date.weekday())
    # start_day = mon.day
    # start_month = mon.month
    # start_year = mon.year
    sun = mon + datetime.timedelta(days=6)
    # end_day = sun.day
    # end_month = sun.month
    # end_year = sun.year

    days = Day.objects.filter(date__gte=mon, date__lte=sun)
    # days = days.filter(year__lte=end_year)
    # days = days.filter(Q(month=start_month, day__gte=start_day) | Q(month=end_month, day__lte=end_day))
    # days = days.filter(date__gte=mon, date__lte=sun)
    days = days.filter(author=request.user)
    days = days.order_by('date')

    hours = Hour.objects.filter(day__in=[d.id for d in days])
    hours = hours.filter(author=request.user)
    hours = hours.order_by('day__date', 'hour')

    # get stats for the template
    total_hours, logged_hours, bad_hours, neutral_hours, good_hours, efficiency = calc_stats(days, hours)
    # pack json data for the template
    json_data = pack_json_data(days, hours, "week")

    output_from = 'Mon %d ' % (mon.day,) + mon.strftime('%b')
    output_to = 'Sun %d ' % (sun.day,) + sun.strftime('%b')
    return render(
        request, 
        'day/week_summary.html', 
        {
            'json_data': json_data,
            'from': output_from,
            'to': output_to,
            'logged_hours': logged_hours,
            'total_hours': total_hours,
            'bad_hours': bad_hours,
            'neutral_hours': neutral_hours,
            'good_hours': good_hours,
            'efficiency': efficiency
        }
    )


@login_required
def month_current(request):
    """ The summary of days this month 
        A basic view of all the logged hours as productivity stats
    """
    today = datetime.datetime.now()
    curr_date = '%d-%d' % (today.month, today.year)    
    return month_by_date(request, curr_date)


@login_required
def month_by_date(request, month_date):
    """ The summary of days from the month defined by the date 
        A basic view of all the logged hours as productivity stats
    """
    month_date = month_date.split('-')  # date format: MM-YYYY
    start = datetime.date(
        day=1,
        month=int(month_date[0]), 
        year=int(month_date[1])
    )
    end = datetime.date(year=start.year, month=start.month+1, day=1) - datetime.timedelta(days=1)
    
    days = Day.objects.filter(date__gte=start, date__lte=end)
    # days = days.filter(year__lte=end.year)
    # days = days.filter(month__gte=start.month)
    # days = days.filter(month__lte=end.month)
    # days = days.filter(day__gte=start.day)
    # days = days.filter(day__lte=end.day)
    days = days.filter(author=request.user)
    days = days.order_by('date')

    hours = Hour.objects.filter(day__in=[d.id for d in days])
    hours = hours.filter(author=request.user)
    hours = hours.order_by('day__date', 'hour')
    
    # get stats for the template
    total_hours, logged_hours, bad_hours, neutral_hours, good_hours, efficiency = calc_stats(days, hours)
    # pack json data for the template
    json_data = pack_json_data(days, hours, "month")

    output_from = start.strftime('%a') + ' %d ' % (start.day,) + start.strftime('%b')
    output_to = end.strftime('%a') + ' %d ' % (end.day,) + end.strftime('%b')

    return render(
        request, 
        'day/month_summary.html', 
        {
            'json_data': json_data,
            'from': output_from,
            'to': output_to,
            'logged_hours': logged_hours,
            'total_hours': total_hours,
            'bad_hours': bad_hours,
            'neutral_hours': neutral_hours,
            'good_hours': good_hours,
            'efficiency': efficiency
        }
    )


@login_required
def tags_summary(request, employer="Myself", tags=None):
    """ The summary days&hours spent on specified tags 
        A basic view of all the logged hours as productivity stats
    """
    tags_output = None
    total_hours = 'N/A'

    form = TagsFilterForm(initial={
        'employer': employer,
        'tags': tags,
    })
    
    # work on everything stats - load everything
    # if main_tag == "Myself":
    #     hours = Hour.objects.filter(author=request.user)
    # specific tags
    # else:
    hours, tags_output = _filter_by_tags(employer, tags)
    hours = hours.filter(author=request.user)

    if tags_output and len(tags_output) > 0 and form.is_valid:
        form.initial['tags'] = tags_output

    # days get loaded depending on already filtered hours
    days = Day.objects.filter(author=request.user)
    days = days.filter(id__in=[h.day.id for h in hours])
    # order by
    # hours = hours.add_extra(order_by='datetime (logs_day.day, logs_hour.month, logs_hour.year)')
    # hours = hours.extra()
    hours = hours.order_by('day__date', 'hour')
    days = days.order_by('date')

    # get stats for the template
    total_hours, logged_hours, bad_hours, neutral_hours, good_hours, efficiency = calc_stats(days, hours)
    # pack json data for the template
    json_data = pack_json_data(days, hours, "overall")
    # adjust chart settings depending on the amount of data
    if len(days) > 30:
        reduce_x_ticks = 'true'
    else:
        reduce_x_ticks = 'false'

    return render(
        request, 
        'day/tags_summary.html', 
        {
            'json_data': json_data,
            'tags': tags_output,
            'employer': employer,
            'logged_hours': logged_hours,
            'total_hours': total_hours,
            'bad_hours': bad_hours,
            'neutral_hours': neutral_hours,
            'good_hours': good_hours,
            'efficiency': efficiency,
            'reduce_x_ticks': reduce_x_ticks,
            'form': form,
        }
    )

@require_http_methods(['POST'])
def tags_filter(request):
    """ Check the form and redirects to the filtered page """
    form = TagsFilterForm(data=request.POST)

    if form.is_valid():
        return redirect(get_tags_path(form))

    return redirect(reverse('tags-summary'))

def _filter_by_tags(employer, tags):

    tags_output = None
    hours = Hour.objects.all()

    # main project tag
    if employer != 'Myself':
        hours = Hour.objects.filter(hour_text__contains=employer)

    # for extra tags present
    if tags is not None:
        # tags = re.split('\W+', 'Words, words, words.')
        tags = tags.split('-')  # tag line format: tag1-tag2-tag3 etc.
        tags_regex = '|'.join(tags)
        tags_output = ', '.join(tags)
        hours = hours.filter(hour_text__regex=r'(' + tags_regex + ')+')
        # DEBUG
        print hours.query

    return hours, tags_output
