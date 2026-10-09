from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # Homepage
    path('', views.job_list, name='job_list'),

    # Job Details
    path('job/<int:pk>/', views.job_detail, name='job_detail'),

    # Create Job
    path('job/create/', views.job_create, name='job_create'),

    # Apply for Job
    path('job/<int:pk>/apply/', views.apply_to_job, name='apply_to_job'),

    # My Applications (NEW)
    path(
        'my-applications/',
        views.my_applications,
        name='my_applications'
    ),

    # Registration
    path('register/', views.register, name='register'),

    # Login
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='jobs/login.html'
        ),
        name='login'
    ),

    # Logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
]