from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Thread, ChatMessage, ReportContact

admin.site.register(ChatMessage)

class ChatMessage(admin.TabularInline):
    model = ChatMessage
    

class ThreadForm(forms.ModelForm):
    def clean(self):
        """
        This is the function that can be used to
        validate your model data from admin
        """
        super(ThreadForm, self).clean()
        first_person = self.cleaned_data.get('first_person')
        second_person = self.cleaned_data.get('second_person')
        if not self.instance.id:
            raise ValidationError(f'Thread between {first_person} and {second_person} already exists.')


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    form = ThreadForm
    list_display = ['first_person', 'second_person', 'blocked']
    list_editable = ['blocked',]
    class Meta:
        model = Thread
        
        
class ReportContactAdmin(admin.ModelAdmin):
    list_display = ['complainant', 'offender', 'subject', 'reason']


admin.site.register(ReportContact, ReportContactAdmin)
admin.site.register(Thread, ThreadAdmin)

