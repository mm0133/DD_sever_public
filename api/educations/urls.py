from django.urls import path
from . import views
app_name = "educations"

urlpatterns = [
    path("eduvideolectures/", views.EduVideoLecturesView.as_view()),
    path("eduvideolectures/<int:pk>/", views.EduVideoLectureView.as_view()),
]