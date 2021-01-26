from django import template

from jobsapp.models import Applicant

register = template.Library()


@register.simple_tag(name='is_already_applied')
def is_already_applied(job, user):
    applied = Applicant.objects.filter(job=job, user=user)
    if applied:
        return True
    else:
        return False

@register.filter(name='get_date')
def get_date(d):
    return d.strftime("%Y-%m-%d")