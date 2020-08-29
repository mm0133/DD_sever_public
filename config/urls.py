"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenObtainSlidingView, \
    TokenRefreshSlidingView
from rest_social_auth.views import SocialJWTPairOnlyAuthView, SocialJWTPairUserAuthView, SocialJWTSlidingOnlyAuthView, \
    SocialJWTSlidingUserAuthView

from api.users.customPipeline import social_signup_profile

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/contests/", include("api.contests.urls")),
    path("api/v1/educations/", include("api.educations.urls")),
    path("api/v1/communications/", include("api.communications.urls")),
    path("api/v1/users/", include("api.users.urls")),
    path("api/v1/managements/", include("api.managements.urls")),

    path("login/social/profile/", social_signup_profile),
    url(r'', include('social_django.urls', namespace='social')),
    #일반로그인 토큰
    path('api/token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    # 소셜로그인 토큰
    url(r'^api/login/social/jwt-sliding/(?:(?P<provider>[a-zA-Z0-9_-]+)/?)?$',
        SocialJWTSlidingOnlyAuthView.as_view(),
        name='login_social_jwt_sliding'),
    # returns token + user_data
    url(r'^api/login/social/jwt-sliding-user/(?:(?P<provider>[a-zA-Z0-9_-]+)/?)?$',
        SocialJWTSlidingUserAuthView.as_view(),
        name='login_social_jwt_sliding_user'),


]

urlpatterns += \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
