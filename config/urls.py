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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_social_auth.views import SocialJWTPairOnlyAuthView, SocialJWTPairUserAuthView

from api.users.customPipeline import social_signup_profile

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/contests/", include("api.contests.urls")),
    path("api/v1/educations/", include("api.educations.urls")),
    path("api/v1/communications/", include("api.communications.urls")),
    path("api/v1/users/", include("api.users.urls")),
    path("api/v1/managements/", include("api.managements.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("login/social/profile/", social_signup_profile),

    url(r'', include('social_django.urls', namespace='social')),
    url(r'^api/login/', include('rest_social_auth.urls_jwt_pair')),


    # returns token only
    url(r'^social/jwt-pair/(?:(?P<provider>[a-zA-Z0-9_-]+)/?)?$',
        SocialJWTPairOnlyAuthView.as_view(),
        name='login_social_jwt_pair'),
    # returns token + user_data
    url(r'^social/jwt-pair-user/(?:(?P<provider>[a-zA-Z0-9_-]+)/?)?$',
        SocialJWTPairUserAuthView.as_view(),
        name='login_social_jwt_pair_user'),

]

urlpatterns += \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
