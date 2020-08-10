from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from social_core.pipeline.partial import partial

from api.users.models import CustomProfile


@partial
def require_profile(strategy, details, user=None, *args, **kwargs):
    if not user:
        if 'password' in kwargs['request'].session:
            return {'email': kwargs['request'].session['email'],
                    'nickname': kwargs['request'].session['nickname'],
                    'phoneNumber': kwargs['request'].session['phoneNumber']}
        else:
            return HttpResponseRedirect(redirect_to='프론트 소셜 사인업 url')
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



@partial
def create_CustomProfile(backend, user, response, is_new=False, *args, **kwargs):
    if is_new:
        CustomProfile.objects.create(
            user=user,
            email=kwargs.get('email'),
            nickname=kwargs.get('nickname'),
            phoneNumber=kwargs.get('phoneNumber'),
        )
