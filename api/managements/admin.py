from django.contrib import admin
from api.managements.models import Notice, QuestionToManager, CommentToQuestion, FeedbackToManager

admin.site.register(Notice)
admin.site.register(QuestionToManager)
admin.site.register(CommentToQuestion)
admin.site.register(FeedbackToManager)


