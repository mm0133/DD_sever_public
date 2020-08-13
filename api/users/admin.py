from django.contrib import admin

from api.users.models import CustomProfile, Team

admin.site.register(CustomProfile)
admin.site.register(Team)
