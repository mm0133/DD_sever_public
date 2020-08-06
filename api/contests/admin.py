from django.contrib import admin

from api.contests.models import Contest, ContestFile, ContestUserAnswer

admin.site.register(Contest)
admin.site.register(ContestFile)
admin.site.register(ContestUserAnswer)

