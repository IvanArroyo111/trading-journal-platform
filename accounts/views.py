from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages

@login_required
def index(request):
    """Dashboard home view for authenticated users."""
    return HttpResponse("You're logged in. Welcome to your dashboard!")

def register(request):
    """User registration view using Django's built-in UserCreationForm."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

@login_required
def settings_view(request):
    """
    Account settings view for updating email, changing password, or deleting account.
    Handles POST requests for each action and provides user feedback via messages.
    """
    user = request.user
    if request.method == "POST":
        # Update Email
        if "email" in request.POST and "old_password" not in request.POST and "delete_account" not in request.POST:
            new_email = request.POST.get("email")
            if new_email and new_email != user.email:
                user.email = new_email
                user.save()
                messages.success(request, "Email updated successfully.")
            else:
                messages.error(request, "Please enter a new email address.")
        # Change Password
        elif "old_password" in request.POST and "new_password1" in request.POST and "new_password2" in request.POST:
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully.")
            else:
                for error in form.errors.values():
                    messages.error(request, error)
        # Delete Account
        elif "delete_account" in request.POST:
            user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect('landing-page')
    return render(request, 'accounts/settings.html')

def landing_page(request):
    """
    Public landing page view.
    Redirects authenticated users to dashboard, otherwise renders landing page with stats and features.
    """
    if request.user.is_authenticated:
        return redirect('dashboard-home')
    stats = [
        {"title": "Traders Joined", "value": "2,500+"},
        {"title": "Trades Logged", "value": "1.2M"},
        {"title": "Avg. Win Rate", "value": "78%"},
        {"title": "Data Privacy", "value": "100%"},
    ]
    features = [
        {
            "img": "images/PreformanceTracking.png",
            "alt": "Performance Tracking",
            "title": "Performance Tracking",
            "desc": "Visualize your trading results with interactive charts and detailed statistics. Identify strengths and weaknesses at a glance."
        },
        {
            "img": "images/StrategyAnalysis.png",
            "alt": "Strategy Analytics",
            "title": "Strategy Analytics",
            "desc": "Deep-dive into your strategies. Filter, tag, and compare trades to discover what works best for you."
        },
        {
            "img": "images/MultiDeviceAccess.png",
            "alt": "Multi-Device",
            "title": "Multi-Device Access",
            "desc": "Access your journal from desktop, tablet, or mobile. Your trades, always in sync and available anywhere."
        },
        {
            "img": "images/SecureAndPrivate.png",
            "alt": "Secure & Private",
            "title": "Secure & Private",
            "desc": "Your data is encrypted and never shared. Focus on trading, knowing your journal is safe and private."
        }
    ]
    return render(request, 'accounts/landing.html', {"stats": stats, "features": features})

def logout_view(request):
    """Logs out the user and redirects to the landing page."""
    logout(request)
    return redirect('landing-page')