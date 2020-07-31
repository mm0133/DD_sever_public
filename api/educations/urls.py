from django.urls import path
from . import views
app_name = "educations"

urlpatterns = [
    path("eduvideolectures/", views.EduVideoLectureView.as_view()),
    path("eduvideolectures/<int:pk>/", views.EduVideoLectureViewWithPk.as_view()),
]