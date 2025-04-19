from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Resume, JobApplication
from .forms import ResumeUploadForm, JobDescriptionForm
from .utils import extract_text_from_file, calculate_match_score

class HomeView(TemplateView):
    template_name = 'core/home.html'

class ResumeUploadView(CreateView):
    model = Resume
    form_class = ResumeUploadForm
    template_name = 'core/upload_resume.html'
    success_url = reverse_lazy('job_description')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        resume = self.object
        resume.text_content = extract_text_from_file(resume.file.path)
        resume.save()
        self.request.session['resume_id'] = resume.id
        return response

class JobDescriptionView(FormView):
    form_class = JobDescriptionForm
    template_name = 'core/upload_resume.html'

    def dispatch(self, request, *args, **kwargs):
        if 'resume_id' not in request.session:
            messages.error(request, "Please upload a resume first.")
            return redirect('upload_resume')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_form'] = True
        return context

    def form_valid(self, form):
        resume_id = self.request.session.get('resume_id')
        resume = Resume.objects.get(id=resume_id)

        job_desc = form.cleaned_data['job_description']
        match_result = calculate_match_score(resume.text_content, job_desc)

        job = JobApplication(
            resume=resume,
            job_title=form.cleaned_data['job_title'],
            company=form.cleaned_data['company'],
            location=form.cleaned_data['location'],
            job_description=job_desc,
            match_percentage=match_result['match_percentage'],
            missing_keywords=', '.join(match_result['missing_keywords'])
        )
        job.save()
        return HttpResponseRedirect(reverse('match_results', args=[job.id]))

class MatchResultsView(DetailView):
    model = JobApplication
    template_name = 'core/match_results.html'
    context_object_name = 'job'

class JobListView(ListView):
    model = JobApplication
    template_name = 'core/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

@require_POST
def update_notes(request, pk):
    job = get_object_or_404(JobApplication, pk=pk)
    job.notes = request.POST.get('notes', '')
    job.save()
    return HttpResponseRedirect(reverse('match_results', args=[pk]))
