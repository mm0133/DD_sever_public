from django.urls import path
from . import views

app_name = "contests"

urlpatterns = [
    path("contest/", views.ContestView.as_view()),
    path("contest/<int:pk>/", views.ContestViewWithPk.as_view()),
    path("contestfile_contest_pk/<int:pk>/", views.ContestFileViewWithContestPK.as_view()),
    path("contestfile_delete/<int:pk>/", views.DeleteContestFileWithPK),
    path("contest_user_answer_contest_pk/<int:pk>/", views.ContestUserAnswerViewWithContestPK.as_view()),
    path("contest_user_answer_pk/<int:pk>/", views.ContestFileViewWithContestPK.as_view()),
]
