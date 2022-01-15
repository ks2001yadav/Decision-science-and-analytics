from django.contrib import admin
from .models import Meet,Profile

class MeetAdmin(admin.ModelAdmin):
    list_display = ('id','starting_time', 'ending_time', 'meeting_link','description', )

admin.site.register(Meet, MeetAdmin)

# admin.site.register(Meet)
admin.site.register(Profile)