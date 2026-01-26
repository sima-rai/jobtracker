from django.urls import path
from . import views

urlpatterns = [
     path("", views.home, name="home"),
     path("dashboard", views.dashboard_view, name="dashboard"),
     path("signup/", views.signup_view, name="signup"),
     path("login/", views.login_view, name="login"),
     path("logout/", views.logout_view, name="logout"),
     path("columns/add", views.add_custom_column, name="add_custom_column"),
     path("jobs/add", views.add_job, name="add_job"),
     path("jobs/<int:job_id>/update/", views.update_job, name="update_job"),
     path("jobs/<int:job_id>/delete/", views.delete_job, name="delete_job"),



]
