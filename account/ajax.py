from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.decorators import login_required
from Minerva.account.forms import ReportForm, EncouragementForm
from Minerva.core.models import Report, Encouragement
from Minerva.core.ajax import clear_validation, show_validation
from datetime import datetime

@dajaxice_register
def form_report(request, form_data, form_id):
    dajax = Dajax()
    form = ReportForm(form_data)
    if form.is_valid():
        clear_validation(dajax, form, form_id)
        data = form.cleaned_data
        message = data['message']
        report = Report()
        report.message = message
        if request.user.is_authenticated():
            report.reporter = request.user.get_profile()
        else:
            report.reporter = None
        report.save()
        dajax.add_data({'status': 'OK'}, 'form_report_callback')
    else:
        clear_validation(dajax, form, form_id)
        show_validation(dajax, form, form_id)
        dajax.add_data({'status': 'INVALID'}, 'form_report_callback')
    return dajax.json()

@dajaxice_register
@login_required
def form_encouragement(request, form_data, form_id):
    dajax = Dajax()
    form = EncouragementForm(form_data)
    if form.is_valid():
        clear_validation(dajax, form, form_id)
        data = form.cleaned_data
        message = data['message']
        person_to = data['person_to']
        anonymous = data['anonymous']
        if person_to != request.user.get_profile():
            encouragement = Encouragement()
            encouragement.message = message
            encouragement.person_to = person_to
            encouragement.person_from = request.user.get_profile()
            encouragement.anonymous = anonymous
            encouragement.sent_time = datetime.now()
            encouragement.save()
            dajax.add_data({'status': 'OK'}, 'form_encouragement_callback')
        else:
            clear_validation(dajax, form, form_id)
            show_validation(dajax, form, form_id)
            dajax.add_data({'status': 'INVALID'}, 'form_encouragement_callback')
    else:
        clear_validation(dajax, form, form_id)
        show_validation(dajax, form, form_id)
        dajax.add_data({'status': 'INVALID'}, 'form_encouragement_callback')
    return dajax.json()
