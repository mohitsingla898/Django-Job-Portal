from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Job, Application
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from django.db.models import Q
from django.http import HttpResponseForbidden

# Display All Jobs
def job_list(request):

    jobs = Job.objects.all().order_by('-created_at')

    query = request.GET.get('q', '').strip()

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query)
        )

    context = {
        'jobs': jobs,
        'query': query
    }

    return render(request, 'jobs/job_list.html', context)


# Display Single Job Details
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    return render(
        request,
        'jobs/job_detail.html',
        {'job': job}
    )
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(
        request,
        'jobs/register.html',
        {'form': form}
    )
# Create New Job
@login_required
def job_create(request):

    if request.method == 'POST':
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)

            job.posted_by = request.user

            job.save()

            return redirect('job_detail', pk=job.pk)

    else:
        form = JobForm()

    return render(
        request,
        'jobs/job_form.html',
        {'form': form}
    )

# Apply for a Job
@login_required
def apply_to_job(request, pk):

    job = get_object_or_404(Job, pk=pk)

    if request.method != 'POST':
        return redirect('job_detail', pk=job.pk)

    if job.posted_by_id == request.user.id:
        messages.error(
            request,
            "You cannot apply to your own job."
        )
        return redirect('job_detail', pk=job.pk)

    application, created = Application.objects.get_or_create(
        job=job,
        applicant=request.user
    )

    if created:
        messages.success(
            request,
            "You have successfully applied for this job!"
        )
    else:
        messages.warning(
            request,
            "You have already applied for this job."
        )

    return redirect('job_detail', pk=job.pk)

# My Job Applications
@login_required
def my_applications(request):

    applications = Application.objects.filter(
        applicant=request.user
    ).select_related('job').order_by('-applied_at')

    return render(
        request,
        'jobs/my_applications.html',
        {'applications': applications}
    )
@login_required
def my_jobs(request):
    jobs = Job.objects.filter(
        posted_by=request.user
    ).order_by('-created_at')

    return render(
        request,
        'jobs/my_jobs.html',
        {'jobs': jobs}
    )
@login_required
def job_edit(request, pk):

    job = get_object_or_404(Job, pk=pk)

    # Only the job owner can edit
    if job.posted_by != request.user:
        return HttpResponseForbidden(
            "You are not allowed to edit this job."
        )

    if request.method == "POST":

        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()

            return redirect('job_detail', pk=job.pk)

    else:
        form = JobForm(instance=job)

    return render(
        request,
        'jobs/job_form.html',
        {
            'form': form,
            'job': job,
            'is_edit': True
        }
    )
@login_required
def job_delete(request, pk):

    job = get_object_or_404(Job, pk=pk)

    # Only the owner can delete the job
    if job.posted_by != request.user:
        return HttpResponseForbidden(
            "You are not allowed to delete this job."
        )

    if request.method == "POST":
        job.delete()
        return redirect('my_jobs')

    return render(
        request,
        'jobs/job_confirm_delete.html',
        {'job': job}
    )