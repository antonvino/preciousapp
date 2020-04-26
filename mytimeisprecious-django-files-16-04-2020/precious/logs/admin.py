from django.contrib import admin
from logs.models import Day, Hour, User, Tag, Download


class HourInline(admin.StackedInline):
    model = Hour
    extra = 0


class HourAdmin(admin.ModelAdmin):
    list_display = ('day', 'hour', 'productive', 'hour_text', 'pub_date', 'author')
    search_fields = ['hour_text', 'hour']


class DayAdmin(admin.ModelAdmin):
    list_display = ('day_text', 'date', 'author')
    search_fields = ['day_text', 'date']
    fieldsets = [
        (None, {'fields': ['day_text']}),
        # ('Date key', {'fields': [('year', 'month'), 'day']}),
        # ('Sync information', {'fields': [('pub_date')], 'classes': ['collapse']}),
    ]
    inlines = [HourInline]


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at', 'is_active')
    search_fields = ['username', 'email']


class TagAdmin(admin.ModelAdmin):
    list_display = ('text', 'author')
    search_fields = ['text']


admin.site.register(Day, DayAdmin)
admin.site.register(Hour, HourAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Download)
