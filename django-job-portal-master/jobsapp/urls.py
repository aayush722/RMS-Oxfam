from django.urls import path, include

from .views import *

app_name = "jobs"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='searh'),
    path('employer/dashboard/', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('all-applicants', ApplicantsListView.as_view(), name='employer-all-applicants'),
        path('applicants/<int:job_id>', ApplicantPerJobView, name='employer-dashboard-applicants'),
        path('csvdump/<int:job_id>', ExportToCsv, name='employer-dashboard-csvdump'),
        path('mark-filled/<int:job_id>', filled, name='job-mark-filled'),
    ])),
    path('apply-job/<int:job_id>', ApplyJobView.as_view(), name='apply-job'),
    path('jobs', JobListView.as_view(), name='jobs'),
    path('jobs/<int:id>', JobDetailsView.as_view(), name='jobs-detail'),
    path('employer/jobs/create', JobCreateView.as_view(), name='employer-jobs-create'),
    path('apply-job-test/<int:job_id>', ApplyJobViewTest.as_view(), name="job-testing"),
]
