from django.urls import path
from . import views
app_name = "educations"

urlpatterns = [
    path("lecturepackage/", views.LecturePackageView.as_view()),
    path("lecturepackage/<int:pk>/", views.LecturePackageViewWithPk.as_view()),
    path("eduvideolecture_with_package_pk/<int:pk>/",
         views.EduVideoLectureViewWithPackagePK.as_view()),
    path("eduvideolecture/<int:pk>/",
         views.EduVideoLectureViewWithVideoPk.as_view()),
]

