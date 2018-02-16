from django.urls import path

from . import views

app_name = 'workouts'
urlpatterns = [
    path('',views.home,name='home'),
    path('new',views.new, name='new'),
    path('create',views.create, name='create'),

    path('session/<int:session_id>',views.detail, name='detail'),
    path('session/<int:session_id>/join',views.join,name='join'),
    path('session/<int:session_id>/leave',views.leave,name='leave'), 
    path('session/<int:session_id>/delete',views.delete,name='delete'),

    path('joined',views.joined, name='joined'),
    path('made',views.made, name='made'),
    path('sessions',views.all, name='all'),
]
