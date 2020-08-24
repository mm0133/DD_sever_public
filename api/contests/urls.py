from django.urls import path
from . import views

app_name = "contests"

urlpatterns = [
    path("contest/", views.ContestView.as_view()),
    path("contest/<int:pk>/", views.ContestViewWithPk.as_view()),
    path("contestfile_with_contest_pk/<int:pk>/", views.ContestFileViewWithContestPK.as_view()),
    path("contestfile_delete/<int:pk>/", views.DeleteContestFileWithPK),
    path("contestparticipantanswer_with_contest_pk/<int:pk>/",
         views.ContestParticipantAnswerViewWithContestPK.as_view()),
    path("contestparticipantanswer/<int:pk>/", views.ContestParticipantAnswerViewWithPK.as_view()),
    path("contest/<int:pk>/scrap/", views.ContestScrap),
    path("contestParticipantAnswer/<int:pk>/like/", views.ContestParticipantAnswerLike),
]
