from django.db import models
from django.utils import timezone
from django import forms
from django.core.validators import RegexValidator

from accounts.models import User

GRADE = (
    ('1', "Chief Executive Officer"),
    ('2', "A-1"),
    ('3', "A-2"),
    ('4', "A-3"),
    ('5', "A-4"),
    ('6', "A-5"),
    ('7', "A-6"),
    ('8', "A-7"),
    ('9', "A-8"),
    ('10', "A-9"),
    ('11', "Consultant"),
    ('12', "Internship"),
    ('13', "Volunteer"),
)

CITY = (
    ('1','Bangalore'),
    ('2','Bhubaneswar'),
    ('3','Delhi'),
    ('4','Kolkata'),
    ('5','Lucknow'),
    ('6','Mumbai'),
    ('7','Patna'),
    ('8','Pune'),
    ('9','Raipur'),
)

JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Consultancy"),
    ('4', "Internship"),
    ('5', "Volunteering Assignment")
)

TRUE_FALSE_CHOICES = (
    ('1', 'Yes'),
    ('2', 'No')
)

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    positions = models.IntegerField(default=1,blank=True)
    description = models.TextField()
    # location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    grade = models.CharField(choices=GRADE,max_length=25)
    experience = models.IntegerField()
    city = models.CharField(choices=CITY, max_length=20)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300)
    # website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    salary = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title

class UserDetials(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicant')
    fullname = models.CharField(max_length=300,default='null')

    email = models.EmailField(blank=False, default='null', unique=True,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be a 10 digit number")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, unique=True,
                                    error_messages={
                                        'unique': "A user with that phone number already exists.",
                                    }) # validators should be a list
    resume = models.FileField()
    date_of_birth = models.DateField()
    highest_qualification = models.TextField(default='null')
    total_experience_yrs = models.IntegerField(default=0)
    total_experience_mos = models.IntegerField(default=0)
    ngo_experience_yrs = models.IntegerField(default=0)
    ngo_experience_mos = models.IntegerField(default=0)
    skill_set = models.TextField(default='null')
    current_ctc = models.IntegerField(default=0)
    expected_ctc = models.IntegerField(default=0)
    notice_period = models.IntegerField(default=0)
    current_org = models.CharField(max_length=300,default='null')
    current_designation = models.CharField(max_length=300,default='null')
    current_city = models.CharField(max_length=300,default='null')
    relocate = models.CharField(choices=TRUE_FALSE_CHOICES, max_length=10,default='null')
    def __str__(self):
        return self.fullname

class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'job']

    def __str__(self):
        return self.user.get_full_name()
