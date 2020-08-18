from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from social_core.pipeline.partial import partial

from api.users.models import CustomProfile


@partial
def request_profile_data(strategy, details, user=None, *args, **kwargs):
    return HttpResponseRedirect(redirect_to='http://127.0.0.1:3000/auth/social_profile/')
    if not user:
        if False:
        # if 'nickname' in kwargs['request'].session:
            return {'email': kwargs['request'].session['email'],
                    'nickname': kwargs['request'].session['nickname'],
                    'phoneNumber': kwargs['request'].session['phoneNumber']}
        else:
            return HttpResponseRedirect(redirect_to='http://127.0.0.1:3000/auth/social_profile/')
    else:
        return


#view 나중에 validation 해도댐
def social_signup_profile(request):
    if request.method == 'POST':
        request.session['email'] = request.POST.get('email')
        request.session['nickname'] = request.POST.get('nickname')
        request.session['phoneNumber'] = request.POST.get('phoneNumber')
        backend = request.session['partial_pipeline']['backend']
        return redirect('social:complete', backend=backend)




def create_CustomProfile(backend, user, response, is_new=False, *args, **kwargs):
    if is_new:
        CustomProfile.objects.create(
            user=user,
            email=kwargs.get('email'),
            nickname=kwargs.get('nickname'),
            phoneNumber=kwargs.get('phoneNumber'),
        )
        return
    else:
        return


# from social_core.pipeline.partial import partial
#
#
# @partial
# def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
#     if kwargs.get('ajax') or user and user.email:
#         return
#     elif is_new and not details.get('email'):
#         email = strategy.request_data().get('email')
#         if email:
#             details['email'] = email
#         else:
#             current_partial = kwargs.get('current_partial')
#             return strategy.redirect(
#                 '/email?partial_token={0}'.format(current_partial.token)
#             )
#
#
# @partial
# def require_country(strategy, details, user=None, is_new=False, *args, **kwargs):
#     if kwargs.get('ajax'):
#         return
#     elif is_new and not details.get('country'):
#         country = strategy.request_data().get('country')
#         if country:
#             details['country'] = country
#         else:
#             current_partial = kwargs.get('current_partial')
#             return strategy.redirect(
#                 '/country?partial_token={0}'.format(current_partial.token)
#             )
#
#
# @partial
# def require_city(strategy, details, user=None, is_new=False, *args, **kwargs):
#     if kwargs.get('ajax'):
#         return
#     elif is_new and not details.get('city'):
#         city = strategy.request_data().get('city')
#         if city:
#             details['city'] = city
#         else:
#             current_partial = kwargs.get('current_partial')
#             return strategy.redirect(
#                 '/city?partial_token={0}'.format(current_partial.token)
#             )
#
#
# SOCIAL_AUTH_PIPELINE = (
#     'social_core.pipeline.social_auth.social_details',
#     'social_core.pipeline.social_auth.social_uid',
#     'social_core.pipeline.social_auth.auth_allowed',
#     'social_core.pipeline.social_auth.social_user',
#     'common.pipeline.require_email',
#     'common.pipeline.require_country',
#     'common.pipeline.require_city',
#     'social_core.pipeline.user.get_username',
#     'social_core.pipeline.mail.mail_validation',
#     'social_core.pipeline.user.create_user',
#     'social_core.pipeline.social_auth.associate_user',
#     'social_core.pipeline.debug.debug',
#     'social_core.pipeline.social_auth.load_extra_data',
#     'social_core.pipeline.user.user_details',
#     'social_core.pipeline.debug.debug'
# )
#
# urlpatterns = [
#     url(r'^$', app_views.home),
#     url(r'^admin/', admin.site.urls),
#     url(r'^email-sent/', app_views.validation_sent),
#     url(r'^login/$', app_views.home),
#     url(r'^logout/$', app_views.logout),
#     url(r'^done/$', app_views.done, name='done'),
#     url(r'^ajax-auth/(?P<backend>[^/]+)/$', app_views.ajax_auth,
#         name='ajax-auth'),
#     url(r'^email/$', app_views.require_email, name='require_email'),
#     url(r'^country/$', app_views.require_country, name='require_country'),
#     url(r'^city/$', app_views.require_city, name='require_city'),
#     url(r'', include('social_django.urls'))
# ]
#
#
#
# from functools import wraps
#
# from django.conf import settings
# from django.shortcuts import render
#
# from common.utils import common_context
#
# from social_django.utils import load_strategy
#
#
# def render_to(template):
#     """Simple render_to decorator"""
#     def decorator(func):
#         """Decorator"""
#         @wraps(func)
#         def wrapper(request, *args, **kwargs):
#             """Rendering method"""
#             out = func(request, *args, **kwargs) or {}
#             if isinstance(out, dict):
#                 out = render(request, template, common_context(
#                     settings.AUTHENTICATION_BACKENDS,
#                     load_strategy(),
#                     request.user,
#                     plus_id=getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
#                     **out
#                 ))
#             return out
#         return wrapper
#     return decorator
#
#
# @render_to('home.html')
# def require_email(request):
#     """Email required page"""
#     strategy = load_strategy()
#     partial_token = request.GET.get('partial_token')
#     partial = strategy.partial_load(partial_token)
#     return {
#         'email_required': True,
#         'partial_backend_name': partial.backend,
#         'partial_token': partial_token
#     }