from django import forms

from .models import UserProfile, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'date_birth', 'about_user', 'photo']
