from django.urls import path
from . import views
app_name = "managements"

urlpatterns = [
    path("", views.foo),
]