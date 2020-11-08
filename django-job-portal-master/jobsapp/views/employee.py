from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView

from accounts.forms import EmployeeProfileUpdateForm
from accounts.models import User
from jobsapp.decorators import user_is_employee
from jobsapp.forms import JobApplyForm
from jobsapp.models import UserDetials, Job
from django.shortcuts import render
from django.forms import modelformset_factory

class EditProfileView(UpdateView):
    model = User
    form_class = EmployeeProfileUpdateForm
    context_object_name = 'employee'
    template_name = 'jobs/employee/edit-profile.html'
    success_url = reverse_lazy('accounts:employer-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

class ApplyJobViewTest(CreateView):
    model = UserDetials
    form_class = JobApplyForm
    slug_field = 'job_id'
    slug_url_kwarg = 'job_id'
    # success_url = reverse_lazy('accounts:login')
    template_name = 'jobs/job_apply.html'

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        # self.object = form.save()
        test_form = form.save(commit=False)
        test_form.job = Job.objects.get(id=self.kwargs['job_id'])
        test_form.save()
        messages.info(self.request, 'Successfully applied for the job!')
        return super().form_valid(test_form)
    
    def get_success_url(self):
        # return reverse_lazy('jobs:jobs-detail', kwargs={'id': self.kwargs['job_id']})
        return reverse_lazy('jobs:home')
