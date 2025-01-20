# projectapp/forms.py
from django import forms

class SearchForm(forms.Form):
    SEARCH_CHOICES = [
        ('year', 'Year'),
        ('document_link', 'Document Link'),
        ('project_id', 'Project ID'),
        ('project_details', 'Project Details'),
    ]
    search_type = forms.ChoiceField(choices=SEARCH_CHOICES)
    search_value = forms.CharField(max_length=100)

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']

# forms.py
from django import forms
from .models import *

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']

# forms.py
from django import forms
from .models import UploadData

class UploadDataForm(forms.ModelForm):
    class Meta:
        model = UploadData
        fields = ['sno', 'name', 'doc_link', 'project_id', 'project_details']

