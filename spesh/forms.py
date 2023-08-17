from django import forms
from .models import PhotoModel
from spesh.models import CustomUser
class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = PhotoModel
        fields = ('image','description')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['userbio', 'profile_pic']
        