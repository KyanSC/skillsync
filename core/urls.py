from django.urls import path
from .views import (
    HomeView,
    ResumeUploadView,
    JobDescriptionView,
    MatchResultsView,
    JobListView,
    update_notes,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('upload/', ResumeUploadView.as_view(), name='upload_resume'),
    path('job-description/', JobDescriptionView.as_view(), name='job_description'),
    path('results/<int:pk>/', MatchResultsView.as_view(), name='match_results'),
    path('jobs/', JobListView.as_view(), name='job_list'),
    path('update-notes/<int:pk>/', update_notes, name='update_notes'),
]
