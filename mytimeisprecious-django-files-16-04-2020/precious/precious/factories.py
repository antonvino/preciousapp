from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from factory import DjangoModelFactory, Sequence
from factory.declarations import SubFactory
from factory.helpers import post_generation
from logs.models import (
    Day, Hour
)

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = Sequence(lambda n: 'user-email-{0}@domain.com.au'.format(n))
    first_name = Sequence(lambda n: 'Emilie {0}'.format(n))
    last_name = Sequence(lambda n: 'Doe {0}'.format(n))
    password = make_password("password")

    # @post_generation
    # def groups(self, create, groups=None, **kwargs):
    #     if not create:
    #         return
    #
    #     if groups:
    #         for group in groups:
    #             self.groups.add(group)


class AdminFactory(UserFactory):
    is_admin = True


############
# Day

class DayFactory(DjangoModelFactory):
    class Meta:
        model = Day

    day_text = Sequence(lambda n: 'Day review {0}'.format(n))
    
    pub_date = now()


############
# Hour

class HourFactory(DjangoModelFactory):
    class Meta:
        model = Hour

    day = SubFactory(DayFactory)
    hour_text = Sequence(lambda n: 'Hour log {0}'.format(n))
    productive = Sequence(lambda n: n)
    pub_date = now()