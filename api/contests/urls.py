from django.urls import path
from . import views

app_name = "contests"

urlpatterns = [
    path("contest/", views.ContestView.as_view()),
    path("contest/<int:pk>/", views.ContestViewWithPk.as_view()),
    path("contest/<int:pk>/scrap/", views.ContestScrap),
    path("contestfile_with_contest_pk/<int:pk>/", views.ContestFileViewWithContestPK.as_view()),
    path("contestfile_delete/<int:pk>/", views.DeleteContestFileWithPK),
    path("contestuseranswer_with_contest_pk/<int:pk>/", views.ContestUserAnswerViewWithContestPK.as_view()),
    path("contestuseranswer/<int:pk>/", views.ContestUserAnswerViewWithPK.as_view()),
]




