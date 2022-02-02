from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, is_safe_url
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from django.urls import reverse


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
