from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("my_page/", views.get_myPage),  # get
    path("profile/<str:nickname>/", views.get_profile),  # get

    path("my_profile/", views.CustomProfileView.as_view()),  # get, post(처음에만), put

    path("team_by_user_nickname/<str:nickname>/", views.get_teams),  # get
    path("team_create/", views.post_team),  # post
    path("team/<str:teamName>/", views.TeamViewWithTeamName.as_view()),  # get put delete

    # path("teaminvite/", views.TeamInviteListView.as_view()),  # get

    path("team/<str:teamName>/member_invite_send/", views.member_invite_send),  # post
    path("team/<str:teamName>/member_invite_accept/", views.member_invite_accept),  # post
    path("team/<str:teamName>/member_invite_cancel/", views.member_invite_cancel),  # post
    path("team/<str:teamName>/member_delete/", views.member_delete),  # post 삭제시 팀대표 자동으로 옮겨줌 팀탈퇴, 대표자가 팀원삭제 모두이거 쓰셈
    path("team/<str:teamName>/change_representative/", views.change_representative),  # post

    path("user_create/", views.UserCreateView.as_view()),
    path("user_delete/", views.delete_user),  # delete 본인회원탈퇴, 프론트에서 토큰 지워주세요
    path("user_delete_admin/<int:pk>/", views.delete_user_pk),  # 관리자용
    path("password_change/", views.ChangePasswordView.as_view()),

    path("has_profile/", views.HasCustomProfile),
    path("check_is_me_staff/", views.check_is_me_staff),
    path("my_basic_information/", views.myBasicInformation),
    path("check_nickname/", views.isProperNickname),

    path("requrie_signup_email_authenticiation/",views.signUpEmailAuthentication),
    path("requrie_findpw_email_authenticiation/", views.findPassWordEmailAuthentication),
    path("confirm_signup_email_authenticiation/", views.signUpEmailAuthenticationConfirm),
    path("confirm_findpw_email_authenticiation/",views.findPassWordEmailAuthenticationConfirm),
]
