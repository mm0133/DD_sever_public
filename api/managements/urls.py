from django.urls import path
from . import views

app_name = "managements"

urlpatterns = [
    path("notice/", views.NoticeListView.as_view()),  # get
    path("notice_create/", views.NoticeCreateView.as_view()),  # post
    path("notice/<int:pk>/", views.NoticeViewWithPk.as_view()),  # get, put, delete
    path("question_to_manager/", views.QuestionToManagerListView.as_view()),  # get
    path("question_to_manager_create/", views.QuestionToManagerCreateView.as_view()),  # post
    path("question_to_manager/<int:pk>/", views.QuestionToManagerViewWithPk.as_view()),
    path("comment_to_question_with_question_pk/<int:pk>/",
         views.CommentToQuestionViewWithQuestionPK.as_view()),
    path("comment_to_question/<int:pk>/",
         views.CommentToQuestionViewWithCommentPK.as_view()),
    path("feedback_to_manager/", views.FeedbackToManagerListView.as_view()),
    path("feedback_to_manager_create/", views.FeedbackToManagerCreateView.as_view()),
    path("feedback_to_manager/<int:pk>/", views.FeedbackToManagerViewWithPk.as_view()),
]
