from django.urls import path
from . import views

app_name = "contests"

urlpatterns = [
    path("contest/", views.ContestListView.as_view()),
    path("contest_unpaginated/", views.ContestListNotPaginatedView.as_view()),
    path("contest_create/", views.ContestCreateView.as_view()),
    path("contest/<int:pk>/", views.ContestViewWithPk.as_view()),
    path("contestfile_with_contest_pk/<int:pk>/", views.ContestFileViewWithContestPK.as_view()),
    path("contestfile_delete/<int:pk>/", views.DeleteContestFileWithPK),
    path("contestparticipantanswer_with_contest_pk/<int:pk>/",
         views.ContestParticipantAnswerListViewWithContestPK.as_view()),
    path("contestparticipantanswer_create_with_contest_pk/<int:pk>/",
         views.ContestParticipantAnswerCreateViewWithContestPK.as_view()),
    path("contestparticipantanswer/<int:pk>/", views.ContestParticipantAnswerViewWithPK.as_view()),
    path("contest/<int:pk>/scrap/", views.ContestScrap),
    path("contestParticipantAnswer/<int:pk>/like/", views.ContestParticipantAnswerLike),
]
