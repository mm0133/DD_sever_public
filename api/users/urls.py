from django.urls import path
from . import views
app_name = "users"

urlpatterns = [
    path("myPage/", views.get_myPage),  # get
    path("profile/<str:nickname>/", views.get_Profile), #get
    path("my_profile/", views.CustomProfileView.as_view()), #get, post(처음에만), put
    path("user_teams/<str:nickname>/", views.get_teams),#get
    path("teams/",views.post_team),#post
    path("teams/<str:teamName>/", views.TeamViewWithTeamName.as_view()), #get delete
    path("teams/<str:teamName>/member_add/", views.member_add),#post
    path("teams/<str:teamName>/member_delete/", views.member_delete),#post 삭제시 팀대표 자동으로 옮겨줌 팀탈퇴, 대표자가 팀원삭제 모두이거 쓰셈
    path("teams/<str:teamName>/change_represetative/", views.change_representative),#post
    path("user_delete/", views.delete_user),#delete 본인회원탈퇴, 프론트에서 토큰 지워주세요
    path("user_delete_admin/<int:pk>/", views.delete_user_pk)#관리자용
]