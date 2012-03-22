from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from crowd.forms import AddSpecializationForm, AddSkillForm, EncouragementForm
from account.models import Profile
from core.models import BadgeAssign, Encouragement


@login_required
def crowd(request, username=None):
    if username == None:
        user = request.user
    else:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
    if user is not None:
        profile = user.get_profile()

        add_specialization_form = AddSpecializationForm(request=request)
        add_skill_form = AddSkillForm(request=request)
        encouragement_form = EncouragementForm(request=request)

        context = RequestContext(request)
        context['viewing_user'] = user
        context['profile'] = profile
        context['badges'] = BadgeAssign.objects.filter(user=user)
        context['encouragements'] = Encouragement.objects.filter(person_to=user).order_by('-sent_time')
        context['related'] = Profile.objects.filter(institute=profile.institute, role='S').exclude(id=request.user.profile.id).exclude(id=profile.id)
        context['add_specialization_form'] = add_specialization_form
        context['add_skill_form'] = add_skill_form
        context['encouragement_form'] = encouragement_form
        return render_to_response('crowd/main.html', context)
    else:
        return HttpResponse('User Not Found!')