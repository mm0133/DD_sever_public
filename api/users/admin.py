from django.contrib import admin

from api.users.models import CustomProfile, Team, TeamInvite

admin.site.register(CustomProfile)
admin.site.register(Team)
admin.site.register(TeamInvite)
