from django import forms
from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    post_text = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Post
        fields = ('patient_Name', 'Blood_group', 'gender', 'Ammount_of_blood', 'patient_types', 'donation_date', 'donation_time', 'Division', 'area', 'hospital_name', 'contact', 'post_text', 'image')

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', 
                            widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))
    class Meta:
        model = Comment
        fields = ('body',)
