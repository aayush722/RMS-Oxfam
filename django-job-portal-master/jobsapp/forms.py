from django import forms
from django.forms import CharField
from jobsapp.models import Job, Applicant, UserDetials


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'created_at','filled')
        labels = {
            "last_date": "Last Date",
            "company_name": "Company Name",
            "company_description": "Company Description"
        }

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        job = super(CreateJobForm, self).save(commit=False)
        if commit:
            job.save()
        return job

class EditJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user','created_at','filled')

class DateInput(forms.DateInput):
    input_type = 'date'

class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('job',)

class JobApplyForm(forms.ModelForm):
    class Meta:
        model = UserDetials
        exclude = ('job',)
        widgets = {'date_of_birth': DateInput(format=['%d/%m/%Y'])}