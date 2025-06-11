from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin

# URL patterns for the accounts app
urlpatterns = [
    # Landing/index page for accounts
    path("", views.index, name="accounts-index"),

    # User registration
    path("register/", views.register, name="register"),

    # Login and logout
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page='landing-page'), name="logout"),

    # Account settings
    path("settings/", views.settings_view, name='account-settings'),

    # Landing page (fallback)
    path('', views.landing_page, name='landing-page'),

    # Admin site URL
    path('admin/', admin.site.urls),
]