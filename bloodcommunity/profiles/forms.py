from django import forms
from .models import Profile

class ProfileModelForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'gender', 'Blood_group_choice', 'donation_activity', 'Last_date_of_donation', 'email','country', 'Division', 'City', 'Area','avatar')