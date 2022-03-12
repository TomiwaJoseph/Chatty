from django.shortcuts import render, redirect
from .models import CustomUser, Profile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, is_safe_url
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import SignupForm, UserUpdateForm, ChangeUserProfile, ChangePasswordForm
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# -------------- Ajax requests --------------------

@login_required
def show_user_profile(request):
    user_profile = CustomUser.objects.get(email=request.user.email)
    return JsonResponse({
        'user_profile': str(user_profile),
        'user_email': user_profile.email,
        'user_picture': user_profile.profile.profile_picture.url,
        'user_status': user_profile.profile.status,
        'user_description': user_profile.profile.description
    })

@login_required
def update_user_profile(request):
    update_form = UserUpdateForm(request.POST, instance=request.user)
    profile_update_form = ChangeUserProfile(
        request.POST, request.FILES,
        instance=Profile.objects.get(user=request.user)
        )
       
    if update_form.is_valid():
        update_form.save()
        
    if profile_update_form.is_valid():
        profile_update_form.save()
        
    return JsonResponse({'status': 'success'})

@login_required
def update_user_password(request):
    change_password_form = ChangePasswordForm(request.POST)
    
    if change_password_form.is_valid():
        email = request.user.email
        old_password = change_password_form.cleaned_data['old_password']
        new_password = change_password_form.cleaned_data['new_password']

        user = authenticate(username=email, password=old_password)
        if user is not None:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return JsonResponse({"status": 'success'})
        else:
            return JsonResponse({"status": 'failure'})
        
# -------------- Ajax requests --------------------

def home(request):
    return render(request, 'registration/home.html')

def sign_in_or_register(request):
    if request.user.is_authenticated:
        return redirect('chathouse')
    if request.method == 'POST':
        sign_up_form = SignupForm(request.POST)
        if sign_up_form.is_valid():
            user = sign_up_form.save(commit=False)
            user.is_active = False
            user.save()
            
            current_site = get_current_site(request).domain
            link = reverse('activate', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            activate_url = current_site + link
            
            mail_subject = 'Activate your WatchnLearn account'
            message = f"Hi {user.first_name}! Please click this link to verify your account\n" + activate_url
            to_email = sign_up_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to = [to_email])
            email.send(fail_silently=True)
            return redirect('awaiting_activation')
    else:
        sign_up_form = SignupForm()
    return render(request, 'registration/login_signup.html', {'sign_up_form': sign_up_form})

def login_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request,
        email=email,
        password=password
    )

    if user is not None:
        login(request, user)
        return redirect('chathouse')
    else:
        messages.error(request, "Invalid Login")
        return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('chathouse')
    else:
        return HttpResponse('Activation link is invalid')

def awaiting_activation(request):
    return render(request, "registration/awaiting_activation.html")
