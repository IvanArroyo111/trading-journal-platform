from django.urls import path
from . import views

# URL patterns for the dashboard app
urlpatterns = [
    # Dashboard home page
    path("", views.dashboard_home, name="dashboard-home"),
]