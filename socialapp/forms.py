from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from socialapp.models import UserProfile,Posts,Comments,Stories


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user","following","block")
        
        widgets={
            "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }

class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["title","post_image"] 

class CommemtForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=["text"]
    

class StoryForm(forms.ModelForm):
    class Meta:
        model=Stories
        fields=["title","post_image"]
        
        
        