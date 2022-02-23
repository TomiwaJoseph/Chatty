from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


# -------------- Ajax requests --------------------

def show_chat_messages(request):
    t = render_to_string('chat/ajax_pages/chat_messages.html')
    return JsonResponse({"conversation": t})

# -------------- Ajax requests --------------------

@login_required
def chathouse(request):
    return render(request, 'chat/welcome_view.html')