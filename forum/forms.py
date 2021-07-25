from django import forms
from .models import UserProfile


class ProfileForm(forms.Form):
    nickname = forms.CharField(label='nickname', max_length=50, required=True)
    profile_picture = forms.ImageField(label='profile_picture', required=False)


class SignupForm(forms.Form):
    nickname = forms.CharField(label='nickname', max_length=50, required=True)
    profile_picture = forms.ImageField(label='profile_picture', required=False)

    def signup(self, request, user):
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.profile_picture = request.FILES['profile_picture']
        print(request.FILES)
        user.save()
        user_profile.save()
