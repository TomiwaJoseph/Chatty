from django import forms


class ReportUserForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'subject',
        'class': 'form-control',
        'placeholder': 'Enter the subject of report...'
    }))
    reason = forms.CharField(widget=forms.Textarea(attrs={
        'id': 'reason',
        'rows': 4,
        'class': 'form-control',
        'placeholder': 'Enter your reason for report...',
    }))
    evidence = forms.ImageField(widget=forms.FileInput(attrs={
        'id': 'evidence',
    }))
    

class AddContactForm(forms.Form):
    contact_email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'contact_email',
        'class': 'form-control',
        'placeholder': "Enter the contact's email"
    }))
