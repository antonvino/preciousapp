from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from logs.views import api
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as rest_views
from registration.backends.default.views import RegistrationView

urlpatterns = []

# if settings.DEBUG:
#     urlpatterns += staticfiles_urlpatterns() \
#         + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ADMIN
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls))
)

# CREATE NEW ACCOUNT
urlpatterns += patterns('logs.views.auth',
    # url(r'^sign_up/$', 'sign_up', name='sign-up'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/register/$',RegistrationView.as_view(template_name='registration/sign_up.html'), name='registration_register'),

)
# BUILT IN ACCOUNT HANDLING
urlpatterns += [
    url('^accounts/login/$', auth_views.login, {'template_name': 'auth/sign_in.html'}, name="login"),
    url('^accounts/logout/$', auth_views.logout, {'next_page': '/accounts/login/'}, name="logout"),
    url('^accounts/password-change/$', auth_views.password_change, {'template_name': 'auth/password_change.html'}, name="password_change"),
    url('^accounts/password-change/done/$', auth_views.password_change_done, {'template_name': 'auth/password_change_done.html'}, name="password_change_done"),
    url('^accounts/password-reset/$', auth_views.password_reset, {'template_name': 'auth/password_reset.html'}, name="password_reset"),
    url('^accounts/password-reset/done/$', auth_views.password_reset_done, {'template_name': 'auth/password_reset_done.html'}, name="password_reset_done"),
    url('^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'template_name': 'auth/password_reset_confirm.html'}, name="password_reset_confirm"),
    url('^accounts/reset/done/$', auth_views.password_reset_complete, {'template_name': 'auth/password_reset_complete.html'}, name="password_reset_complete"),
]

# SYNC
urlpatterns += patterns('logs.views.sync',
    url(r'^sync$', 'sync_json', name='sync-json'),
    url(r'^sync_mac$', 'sync_mac', name='sync-mac'),
)

# DAY VIEWS
urlpatterns += patterns('logs.views.day_views',

    # WEEKS
    url(r'^week/$', 'week_current', name='week-current'),
    url(r'^week/(?P<week_date>[-\w]+)/$', 'week_by_date', name="week-by-date"),

    # MONTHS
    url(r'^month/$', 'month_current', name='month-current'),
    url(r'^month/(?P<month_date>[-\w]+)/$', 'month_by_date', name="month-by-date"),

    # TAGS
    url(r'^tags/filter/$', 'tags_filter', name='tags-filter'),
    url(r'^tags/for:(?P<employer>[-\w]+)/$', 'tags_summary', name="tags-employer"),
    url(r'^tags/for:(?P<employer>[-\w]+)/tags:(?P<tags>[-\w]+)/$', 'tags_summary', name="tags-employer-tags"),
    # url(r'^tags/tags:(?P<tags>[-\w]+)/$', 'tags_summary', name="tags-tags"),
    # url(r'^tags/tags:(?P<other_tags>[-\w]+)/$', 'tags_summary', name="tags-summary"),
    # url(r'^tags/(?P<main_tag>[-\w]+)', 'tags_summary', name="tags-summary"),
    url(r'^tags/$', 'tags_summary', name="tags-summary"),
)

urlpatterns += [
    url(r'^api/hours/$', api.HourList.as_view(), name="hours-list"),
    url(r'^api/hours/(?P<pk>[0-9]+)/$', api.HourDetail.as_view(), name="hour-detailed"),
    url(r'^api/days/$', api.DayList.as_view(), name="days-list"),
    url(r'^api/days/(?P<pk>[0-9]+)/$', api.DayDetail.as_view(), name="day-detailed"),
    url(r'^api/users/$', api.UserList.as_view(), name="users-list"),
    url(r'^api/users/(?P<pk>[0-9]+)/$', api.UserDetail.as_view(), name="user-detailed"),
    url(r'^api/sign-up/$', api.UserCreate.as_view(), name="user-create"),
]

urlpatterns = format_suffix_patterns(urlpatterns)


urlpatterns += patterns('',
    # API auth
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    url(r'^api/token-auth/$', api.UserObtainAuthToken.as_view(), name="token-auth"),

)

# additional pages
urlpatterns += patterns('logs.views.misc',
    url(r'^$', 'main', name='default'),  # DEFAULT
    url(r'^terms$', 'terms', name="terms"),
    url(r'^privacy$', 'privacy', name="privacy"),
    url(r'^download$', 'download', name="download"),
)