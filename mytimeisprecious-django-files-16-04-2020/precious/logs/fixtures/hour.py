from django.utils.text import slugify
from apf.factories import HourFactory
from apf.models import Hour

def load_resources():
    for hour_index in range(0, 45):
        HourFactory.create()
        