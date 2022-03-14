from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from users.models import Profile, CustomUser
from users.forms import UserUpdateForm, ChangeUserProfile, ChangePasswordForm
from .models import Thread, ReportContact, ChatMessage
from .forms import ReportUserForm, AddContactForm
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from django.core.mail import EmailMultiAlternatives, EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q


# -------------- Ajax requests --------------------

@login_required
def show_contact_profile(request):
    other_user =  int(request.GET.get('other_user_id'))
    user_profile = CustomUser.objects.get(id=other_user)
    return JsonResponse({
        'user_profile': str(user_profile),
        'user_email': user_profile.email,
        'user_picture': user_profile.profile.profile_picture.url,
        'user_status': user_profile.profile.status,
        'user_description': user_profile.profile.description
    })

@login_required
def report_contact(request):
    other_user =  int(request.POST.get('other_user_id'))
    user_profile = CustomUser.objects.get(id=other_user)
    the_subject = request.POST.get('subject')
    the_reason = request.POST.get('reason')
    the_evidence = request.FILES.get('evidence')
    
    # Report logic goes here...
    the_report = ReportContact.objects.create(
        complainant=request.user,
        offender=user_profile,
        subject=the_subject,
        reason=the_reason,
        evidence=the_evidence
    )
    # the_report = ReportContact.objects.get(id=2)
    
    body_html = the_reason
    from_email = request.user.email
    to_email = settings.EMAIL_HOST_USER
    
    msg = EmailMultiAlternatives(
        the_subject,
        body_html,
        from_email=from_email,
        to=[to_email]
    )
    msg.content_subtype = 'html'
    msg.mixed_subtype = 'related'
    msg.attach_alternative(body_html, 'text/html')
    image = MIMEImage(the_report.evidence.read())
    image.add_header('Content-ID', "<{}>".format(the_report.evidence))
    msg.attach(image)
    msg.send()
    
    return JsonResponse({'the_contact': str(user_profile)})

@login_required
def add_contact(request):
    new_user = AddContactForm(request.POST)
    if new_user.is_valid():
        new_contact = new_user.cleaned_data['contact_email']
        other_user = CustomUser.objects.filter(email=new_contact)
        if not other_user.exists():
            return JsonResponse({'status': 'unknown contact'})
        else:
            if other_user.first() == request.user:
                return JsonResponse({'status': 'same user'})
            qs = Thread.objects.filter(
                (Q(first_person=other_user.first().id) | Q(second_person=other_user.first().id)) &
                (Q(first_person=request.user.id) | Q(second_person=request.user.id))
                )
            if qs and qs.first().blocked:
                return JsonResponse({'status': 'blocked thread'})
            elif qs and (qs.first().blocked == False):
                return JsonResponse({'status': 'existing thread'})
            else:
                Thread.objects.create(
                    first_person = request.user,
                    second_person = other_user.first(),
                )
    
    return JsonResponse({'status': 'success'})

# -------------- Ajax requests --------------------

@login_required
def chathouse(request):
    profile_object = Profile.objects.get(user=request.user).profile_picture
    logged_user_picture = profile_object.url
    user_update_form = UserUpdateForm(instance=request.user)
    user_profile_update_form = ChangeUserProfile(
        instance=Profile.objects.get(user=request.user)
        )
    change_password_form = ChangePasswordForm()
    report_user_form = ReportUserForm()
    add_contact_form = AddContactForm()
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('-timestamp')
    context = {
        "logged_user_picture": logged_user_picture,
        "Threads": threads,
        "user_update_form": user_update_form,
        "user_profile_update_form": user_profile_update_form,
        "change_password_form": change_password_form,
        "report_user_form": report_user_form,
        "add_contact_form": add_contact_form,
    }
    return render(request, 'chat/welcome_view.html', context)

