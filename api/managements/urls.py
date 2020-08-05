from django.urls import path
from . import views
app_name = "managements"

urlpatterns = [
    path("notice/", views.NoticeView.as_view()), #get, post
    path("notice_pinned/", views.pinnedNotice), #get
    path("notice_not_pinned/", views.notpinnedNotie), #get
    path("notice/<int:pk>/",views.NoticeViewWithPk.as_view()), #get, put, delete
    path("question_to_manager_private/", views.get_privateQuestionToManager),#get
    path("question_to_manager_public/",views.get_publicQuestionToManager),#get
    path("question_to_manager/",views.register_QuestionToManager),#post
    path("question_to_manager/<int:pk>/", views.QuestionToManagerViewWithPk.as_view()),
    path("comment_to_question_question_pk/<int:pk>/",views.CommentToQuestionViewWithQuestionPK.as_view()),
    path("comment_to_question/<int:pk>/", views.CommentToQuestionViewWithPK.as_view()),
    path("feedback_to_manager/",views.FeedbackToManagerView.as_view()),
    path("feedback_to_manager/<int:pk>/",views.CommentToQuestionViewWithPK.as_view()),

]