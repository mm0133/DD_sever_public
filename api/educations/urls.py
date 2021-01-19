from django.urls import path
from . import views

app_name = "educations"

urlpatterns = [
    path("lecturepackage/", views.LecturePackageListView.as_view()),
    path("lecturepackage_create/", views.LecturePackageCreateView.as_view()),
    path("lecturepackage/<int:pk>/", views.LecturePackageViewWithPk.as_view()),
    path("eduvideolecture_with_package_pk/<int:pk>/", views.EduVideoLectureViewWithPackagePK.as_view()),
    path("eduvideolecture/<int:pk>/", views.EduVideoLectureViewWithVideoPk.as_view()),

    path("lecturepackagecomment_with_package_pk/<int:pk>/", views.LecturePackageCommentsViewWithPackagePK.as_view()),
    path("lecturepackagecomment/<int:pk>/", views.LecturePackageCommentsViewWithPK.as_view()),
    path("lecturepackagecomment/<int:pk>/like/", views.LecturePackageCommentLike),

    path("eduVideoLectureComment_with_package_pk/<int:pk>/", views.EduVideoLectureCommentsViewWithVideoPK.as_view()),
    path("eduVideoLectureComment/<int:pk>/", views.EduVideoLectureCommentViewWithPK.as_view()),
    path("eduVideoLectureComment/<int:pk>/like/", views.EduVideoLectureCommentLike),

    path("lecturenotecomment_with_page/<str:page>/", views.LectureNoteCommentViewWithPage.as_view()),
    path("lecturenotecomment/<int:pk>/", views.LectureNoteCommentViewWithPK.as_view()),
    path("lecturenotecomment/<int:pk>/like/", views.LectureNoteCommentLike),
]
