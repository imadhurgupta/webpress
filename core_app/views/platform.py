from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ..forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.conf import settings
from ..models import Website, Profile, Lead
import random

# ─── Public & Platform Views ───────────────────────────────────────────────────

def overview(request):
    return render(request, 'core_app/platform/overview.html', {'title': 'Website Overview'})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'core_app/platform/login.html', {'title': 'Login'})

def logout_view(request):
    logout(request)
    return redirect('overview')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate until OTP is verified
            user.save()
            otp = str(random.randint(100000, 999999))
            request.session['signup_user_id'] = user.id
            request.session['signup_otp'] = otp
            try:
                from django.core.mail import EmailMultiAlternatives
                from django.template.loader import render_to_string
                from django.utils.html import strip_tags
                html_content = render_to_string('core_app/platform/emails/email_otp.html', {'otp': otp})
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives('Your WebPress Verification Code', text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=False)
                messages.success(request, 'An OTP has been sent to your email. Please verify to continue.')
            except Exception as e:
                messages.error(request, f'Failed to send OTP email: {str(e)}')
            return redirect('verify_otp')
        for field, errors in form.errors.items():
            for error in errors: messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'core_app/platform/signup.html', {'title': 'Sign Up', 'form': form})

def verify_otp_view(request):
    if request.user.is_authenticated: return redirect('dashboard')
    user_id = request.session.get('signup_user_id')
    stored_otp = request.session.get('signup_otp')
    if not user_id or not stored_otp:
        messages.error(request, 'No active signup session found.')
        return redirect('signup')
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        if entered_otp == stored_otp:
            try:
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()
                del request.session['signup_user_id']; del request.session['signup_otp']
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Welcome, {user.username}! Your email has been verified.')
                return redirect('dashboard')
            except User.DoesNotExist: return redirect('signup')
        else: messages.error(request, 'Invalid OTP.')
    return render(request, 'core_app/platform/verify_otp.html', {'title': 'Verify OTP'})

@login_required(login_url='login')
def dashboard(request):
    websites = Website.objects.filter(user=request.user)
    leads_count = Lead.objects.filter(website__user=request.user).count()
    return render(request, 'core_app/platform/dashboard.html', {
        'user': request.user, 'websites': websites, 'leads_count': leads_count
    })

@login_required(login_url='login')
def profile_view(request):
    u_form = UserUpdateForm(instance=request.user)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    p_form = ProfileUpdateForm(instance=profile)
    pwd_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save(); p_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('profile')
        elif 'change_password' in request.POST:
            pwd_form = PasswordChangeForm(request.user, request.POST)
            if pwd_form.is_valid():
                user = pwd_form.save(); update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
    return render(request, 'core_app/platform/profile.html', {
        'u_form': u_form, 'p_form': p_form, 'pwd_form': pwd_form, 'title': 'User Profile'
    })

@login_required(login_url='login')
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(); update_session_auth_hash(request, user)
            messages.success(request, 'Password updated!')
            return redirect('profile')
    else: form = PasswordChangeForm(request.user)
    return render(request, 'core_app/platform/change_password.html', {'form': form, 'title': 'Change Password'})

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'core_app/platform/auth/password_reset.html'
    email_template_name = 'core_app/platform/emails/password_reset_email.txt'
    html_email_template_name = 'core_app/platform/emails/password_reset_email.html'
    subject_template_name = 'core_app/platform/emails/password_reset_subject.txt'
    success_url = '/password-reset/done/'

# ─── Error Handlers ────────────────────────────────────────────────────────────

def error_404(request, exception):
    return render(request, 'core_app/platform/error.html', {'code': 404, 'title': 'Page Not Found', 'message': "The page you're looking for doesn't exist or has been moved."}, status=404)

def error_500(request):
    return render(request, 'core_app/platform/error.html', {'code': 500, 'title': 'Server Error', 'message': 'Something went wrong on our end. Please try again in a moment.'}, status=500)
