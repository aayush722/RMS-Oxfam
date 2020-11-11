from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from django.shortcuts import render, redirect
from jobsapp.decorators import user_is_employer
from jobsapp.forms import CreateJobForm
from jobsapp.models import Job, Applicant, UserDetials
from jobsapp.filters import ApplicantFilter
import csv
import xlwt


class DashboardView(ListView):
    model = Job
    template_name = 'jobs/employer/dashboard.html'
    context_object_name = 'jobs'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)

def ExportToCsv(request, **kwargs):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="applicants.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['First Name', 'Last Name', 'Degree']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = UserDetials.objects.filter(job_id=kwargs['job_id']).values_list('firstname', 'lastname', 'degree')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def ApplicantPerJobView(request, **kwargs):
    # TODO CHECK FEASABILITY: changed from ListView to normal function  
	applicants = UserDetials.objects.filter(job_id=kwargs['job_id']).order_by('id')

	myFilter = ApplicantFilter(request.GET, queryset=applicants)
	applicants = myFilter.qs 

	context = {'applicants':applicants,'myFilter':myFilter, 'job_id':kwargs['job_id']}
	return render(request, 'jobs/employer/applicants.html',context)



class JobCreateView(CreateView):
    template_name = 'jobs/create.html'
    form_class = CreateJobForm
    extra_context = {
        'title': 'Post New Job'
    }
    success_url = reverse_lazy('jobs:employer-dashboard')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ApplicantsListView(ListView):
    model = Applicant
    template_name = 'jobs/employer/all-applicants.html'
    context_object_name = 'applicants'

    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        return self.model.objects.filter(job__user_id=self.request.user.id)


@login_required(login_url=reverse_lazy('accounts:login'))
def filled(request, job_id=None):
    try:
        job = Job.objects.get(user_id=request.user.id, id=job_id)
        job.filled = True
        job.save()
    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))
    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))
