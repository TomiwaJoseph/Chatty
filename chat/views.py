from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .models import Thread


@login_required
def chathouse(request):
    profile_object = Profile.objects.get(user=request.user).profile_picture
    logged_user_picture = profile_object.url
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        "logged_user_picture": logged_user_picture,
        "Threads": threads,
    }
    return render(request, 'chat/welcome_view.html', context)