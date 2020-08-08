from django.urls import path
from . import views
app_name = "communications"

urlpatterns = [
    path("contestdebate/", views.ContestDebateView.as_view()),
    path("contestdebate/<int:pk>/", views.ContestDebateViewWithPk.as_view()),
    path("contestdebate/<int:pk>/like/", views.ContestDebateLike),
    path("contestdebate/<int:pk>/scrap/", views.ContestDebateScrap),
    path("contestcodenote/", views.ContestCodeNoteView.as_view()),
    path("contestcodenote/<int:pk>/", views.ContestCodeNoteViewWithPk.as_view()),
    path("contestcodenote/<int:pk>/like/", views.ContestCodeNoteLike),
    path("contestcodenote/<int:pk>/scrap/", views.ContestCodeNoteLike),
    path("velog/", views.VelogView.as_view()),
    path("velog/<int:pk>/", views.VelogViewWithPk.as_view()),
    path("velog/<int:pk>/like/", views.VelogLike),
    path("velog/<int:pk>/scrap/", views.VelogScrap),
    path("debatecomment_with_debate_pk/<int:pk>/",views.DebateCommentViewWithDebatePK.as_view()),
    path("debatecomment/<int:pk>/",views.DebateCommentViewWithPK.as_view()),
    path("debatecomment/<int:pk>/like/", views.DebateCommentLike),
    path("codenotecomment_codenote_pk/<int:pk>/",views.CodeNoteCommentViewWithCodeNotePK.as_view()),
    path("codenotecomment/<int:pk>/",views.CodeNoteCommentViewWithPK.as_view()),
    path("codenotecomment/<int:pk>/like/", views.CodeNoteCommentLike),
    path("velogComment_with_velog_pk/<int:pk>/",views.VelogCommentViewWithVelogPK.as_view()),
    path("velogComment/<int:pk>/", views.VelogViewWithPk.as_view()),
    path("velogComment/<int:pk>/like")
]