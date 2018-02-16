from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views import generic
from django.urls import reverse
from django.utils import timezone

from .models import WorkoutSession
from .forms import WorkoutSessionForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request,'workouts/signup.html',{'form':form})

def home(request):
    return render(request,'workouts/home.html', {
        'user' : request.user,
    })

def all(request):
    template_name = 'workouts/list_sessions.html'
    all_sessions = WorkoutSession.objects.all()
    return render(request,template_name, {
        'sessions' : all_sessions
    })

@login_required
def joined(request):
    template_name = 'workouts/list_sessions.html'
    all_sessions = WorkoutSession.objects.all()
    sesh_ids = set()
    for sesh in all_sessions:
        if request.user == sesh.created_by:
            sesh_ids.add(sesh.id)
        for attendant in sesh.attendees.all():
            if attendant == request.user:
                sesh_ids.add(sesh.id)
    joined_sessions = WorkoutSession.objects.all().filter(id__in=list(sesh_ids))
    return render(request,template_name, {
        'sessions' : joined_sessions
    })

@login_required
def made(request):
    template_name = 'workouts/list_sessions.html'
    made = WorkoutSession.objects.all().filter(
        created_by=request.user
    )
    return render(request,template_name, {
        'sessions' : made
    })

@login_required
def create(request):
    if request.method == "POST":
        data = request.POST
        sesh = WorkoutSession(
            name=data['name'],
            description=data['description'],
            location=data['location'],
            pub_date=timezone.now(),
            workout_date=data['workout_date'],
            created_by=request.user
        )
        sesh.save()
        return render(request,'workouts/session_made.html')
    else:
        return redirect('/')

@login_required
def join(request,session_id):
    session = WorkoutSession.objects.get(pk=session_id)
    if (session.created_by != request.user):
        session.attendees.add(request.user)
        session.save()
    return render(request,'workouts/operation_complete.html')


@login_required
def leave(request,session_id):
    session = WorkoutSession.objects.get(pk=session_id)
    if (session.created_by != request.user):
        session.attendees.remove(request.user)
        session.save()
    return render(request,'workouts/operation_complete.html')

@login_required
def delete(request,session_id):
    session = WorkoutSession.objects.get(pk=session_id)
    if (session.created_by == request.user):
        session.delete()
    return render(request,'workouts/operation_complete.html')

@login_required
def new(request):
    form = WorkoutSessionForm()
    return render(request,'workouts/create_session.html', {
        'form' : form
        })

def detail(request,session_id):
    all_sessions = WorkoutSession.objects.all()
    sesh_ids = set()
    for sesh in all_sessions:
        if request.user == sesh.created_by:
            sesh_ids.add(sesh.id)
        for attendant in sesh.attendees.all():
            if attendant == request.user:
                sesh_ids.add(sesh.id)

    sesh_ids = list(sesh_ids)
    session = get_object_or_404(WorkoutSession, pk=session_id) 
    return render(request,'workouts/workout_details.html',{
        'session' : session,
        'request' : request,
        'sesh_ids' : sesh_ids
    })
