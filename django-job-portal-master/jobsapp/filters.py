import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class ApplicantFilter(django_filters.FilterSet):
	firstname = CharFilter(field_name='firstname', lookup_expr='icontains')
	class Meta:
		model = UserDetials
		fields = ['firstname',]
		# exclude = ['resume']