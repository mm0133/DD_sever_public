from django.contrib import admin

from api.communications.models import ContestDebate, ContestCodeNote, Velog, DebateComment, CodeNoteComment, \
    VelogComment

admin.site.register(ContestDebate)
admin.site.register(ContestCodeNote)
admin.site.register(Velog)
admin.site.register(DebateComment)
admin.site.register(CodeNoteComment)
admin.site.register(VelogComment)