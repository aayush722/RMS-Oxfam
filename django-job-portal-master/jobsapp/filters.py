import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class ApplicantFilter(django_filters.FilterSet):
	fullname = CharFilter(field_name='fullname', lookup_expr='icontains')
	class Meta:
		model = UserDetials
		fields = ['fullname',]
		# exclude = ['resume']