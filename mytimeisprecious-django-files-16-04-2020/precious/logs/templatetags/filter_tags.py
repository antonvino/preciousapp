from django import template
from django.core.urlresolvers import reverse
from logs.forms.filter_forms import TagsFilterForm

register = template.Library()


@register.simple_tag
def get_tags_path(form):
    """
    Turns the TagsFilterForm into a nice URL.
    ex: /tags/employer:precious/tags:precious_web-precious_app
    """
    assert form.__class__ == TagsFilterForm, \
        "The tag `get_tags_path` excepts a TagsFilterForm instance"

    # tags URL part
    if(form['tags'].value()):
        tags = str(form['tags'].value().replace(', ','-').replace(' ','-'))
    else:
        tags = None
    # employer URL part
    employer = 'Myself'
    if(form['employer']):
        employer = str(form['employer'].value())
    if(len(employer) < 1):
        employer = 'Myself'
    print 'tags:{0}, employer:{1}'.format(tags, employer)

    # reverse the tags-employer views
    if tags is not None:
        url_kwargs = {
            'employer': employer,
            'tags': tags
        }
        return reverse('tags-employer-tags', kwargs=url_kwargs)
    else:
        url_kwargs = {
            'employer': employer
        }
        return reverse('tags-employer', kwargs=url_kwargs)



