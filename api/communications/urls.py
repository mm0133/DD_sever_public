from django.urls import path
from . import views
app_name = "communications"

urlpatterns = [
    path("contestdebate/", views.ContestDebateView.as_view()),
    path("contestdebate/<int:pk>/", views.ContestDebateViewWithPk.as_view()),
]