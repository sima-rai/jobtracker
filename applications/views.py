from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import JobApplications, CustomColumn
from datetime import date
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
# Create your views here.



def hello_world(self):
    return HttpResponse("Hello world")



def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'applications/home.html')

@login_required
def dashboard_view(request):
    user = request.user
    query = request.GET.get("search", "").strip()
    filter_status = request.GET.get("filter", "")

    jobs = JobApplications.objects.filter(user=user)


    if filter_status and filter_status != "all":
        jobs = jobs.filter(status = filter_status)

    metrics = JobApplications.objects.filter(user=user).aggregate(
        jobs_total = Count('id'),
        jobs_applied=Count('id', filter=Q(status='Applied')),
        jobs_rejected=Count('id', filter=Q(status='Rejected')),
        jobs_pending=Count('id', filter=Q(status='Pending')),
        jobs_interview=Count('id', filter=Q(status='Interview')),
    )
    
    if query:
        jobs = jobs.filter(
            Q(company__icontains=query) |
            Q(position__icontains=query) |
            Q(notes__icontains=query) |
            Q(status__icontains=query)|
            Q(applied_on__icontains=query)

        )

    jobs = jobs.order_by("-created_at")
    columns = CustomColumn.objects.filter(user=user)

    paginator = Paginator(jobs, 10)
    page_number = request.GET.get("page")
    jobs = paginator.get_page(page_number)


    return render(request, 'applications/dashboard.html', {
        'jobs':jobs, 
        'columns':columns, 
        'search_query':query, 
        'metrics': metrics,
        'filter_status': filter_status,  #send to template for highlighting
        })


@login_required
def add_job(request):
    if request.method == 'POST':
        JobApplications.objects.create(
            user=request.user,
            company=request.POST.get('company'),
            url_link=request.POST.get('url_link'),
            position=request.POST.get('position'),
            status=request.POST.get('status'),
            notes=request.POST.get('notes'),
            applied_on=request.POST.get('applied_on') or date.today(),
        )
    
    return redirect('dashboard')



@login_required
@require_POST
def update_job(request, job_id):
    job = get_object_or_404(JobApplications, id=job_id, user=request.user)
    job.applied_on = request.POST.get("applied_on")
    job.company = request.POST.get("company")
    job.url_link = request.POST.get("url_link")
    job.position = request.POST.get("position")
    job.status = request.POST.get("status")
    job.notes = request.POST.get("notes")

    job.save()



    return JsonResponse({
        "success":True,
        "job":{
            "applied_on": job.applied_on,
            "company": job.company,
            "url_link": job.url_link,
            "position": job.position,
            "status": job.status,
            "notes": job.notes,
        }
    })

@login_required
@require_POST
def delete_job(request, job_id):
    job = get_object_or_404(JobApplications, id=job_id, user=request.user)
    job.delete()
    return JsonResponse({"success":True})




@login_required
def add_custom_column(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        field_type = request.POST.get('field_type')

        CustomColumn.objects.create(
            user = request.user,
            name = name,
            field_type = field_type,
        )
        return redirect('dashboard')



def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        return redirect("dashboard")
    return render(request, 'applications/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
        
    return render(request, 'applications/login.html')

def logout_view(request):
    logout(request)
    return redirect("home")