from django.shortcuts import render


def chathouse(request):
    return render(request, 'chat/chathouse.html')