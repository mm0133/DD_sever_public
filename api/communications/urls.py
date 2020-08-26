from django.urls import path
from . import views

app_name = "communications"

urlpatterns = [
    path("contestdebate/", views.ContestDebateListView.as_view()),
    path("contestdebate_with_contest_pk/<int:pk>/", views.ContestDebateListViewWithContestPK.as_view()),
    path("contestdebate_create_with_contest_pk/<int:pk>/", views.ContestDebateCreateWithContestPk),
    path("contestdebate/<int:pk>/", views.ContestDebateViewWithPk.as_view()),
    path("contestdebate/<int:pk>/like/", views.ContestDebateLike),
    path("contestdebate/<int:pk>/scrap/", views.ContestDebateScrap),

    path("contestcodenote/", views.ContestCodeNoteListView.as_view()),
    path("contestcodenote_/<int:pk>/", views.ContestCodeNoteListViewWithContestPK.as_view()),
    path("contestcodenote_create_with_contest_pk/<int:pk>/", views.ContestCodeNoteCreateWithContestPk),
    path("contestcodenote/<int:pk>/", views.ContestCodeNoteViewWithPk.as_view()),
    path("contestcodenote/<int:pk>/like/", views.ContestCodeNoteLike),
    path("contestcodenote/<int:pk>/scrap/", views.ContestCodenoteScrap),

    path("velog/", views.VelogListView.as_view()),
    path("velog_create/", views.VelogView.as_view()),
    path("velog/<int:pk>/", views.VelogViewWithPk.as_view()),
    path("velog/<int:pk>/like/", views.VelogLike),
    path("velog/<int:pk>/scrap/", views.VelogScrap),

    path("debatecomment_with_debate_pk/<int:pk>/", views.DebateCommentViewWithDebatePK.as_view()),
    path("debatecomment/<int:pk>/", views.DebateCommentViewWithPK.as_view()),
    path("debatecomment/<int:pk>/like/", views.DebateCommentLike),

    path("codenotecomment_with_codenote_pk/<int:pk>/", views.CodeNoteCommentViewWithCodeNotePK.as_view()),
    path("codenotecomment/<int:pk>/", views.CodeNoteCommentViewWithPK.as_view()),
    path("codenotecomment/<int:pk>/like/", views.CodeNoteCommentLike),

    path("velogcomment_with_velog_pk/<int:pk>/", views.VelogCommentViewWithVelogPK.as_view()),
    path("velogcomment/<int:pk>/", views.VelogCommentViewWithPK.as_view()),
    path("velogcomment/<int:pk>/like/", views.VelogCommentLike)
]
