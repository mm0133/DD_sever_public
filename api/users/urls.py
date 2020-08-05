from django.urls import path
from . import views
app_name = "users"

urlpatterns = [
    path("profile/<str:nickname>/", views.get_Profile), #get
    path("my_profile/", views.CustomProfileView.as_view()), #get, post(처음에만), put
]