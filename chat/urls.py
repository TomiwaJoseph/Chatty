from django.urls import path
from . import views


urlpatterns = [
    path('chat/', views.chathouse, name='chathouse'),
    
    # -------------- Ajax requests --------------------
    path('show_chat_messages/', views.show_chat_messages),
    # -------------- Ajax requests --------------------
]
