from django.utils.text import slugify
from apf.factories import DayFactory
from apf.models import Day

def load_resources():
    for day_index in range(0, 45):
        DayFactory.create()
        