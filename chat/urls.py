from django.urls import path
from . import views


urlpatterns = [
    path('chat/', views.chathouse, name='chathouse'),
    
    # -------------- Ajax requests --------------------
    path('show_contact_profile/', views.show_contact_profile),
    path('report_contact/', views.report_contact),
    path('add_contact/', views.add_contact),
    path('search_chat/', views.search_chat),
    # -------------- Ajax requests -------------------
]
