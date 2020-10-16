from django.db import models
from django.utils import timezone
from django import forms

from accounts.models import User

JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    salary = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title

class UserDetials(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicant')
    firstname = models.CharField(max_length=300)
    lastname = models.CharField(max_length=300)

    # email = models.EmailField(unique=True, blank=False,
    #                           error_messages={
    #                               'unique': "A user with that email already exists.",
    #                           })
    resume = models.FileField()
    date_of_birth = models.DateField(blank=True, null=True)
    degree = models.CharField(max_length=300)
    institute = models.CharField(max_length=300)
    department = models.CharField(max_length=300)
    def __str__(self):
        return self.firstname

class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'job']

    def __str__(self):
        return self.user.get_full_name()
