from django import forms
from .models import *
from django.templatetags.static import static


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ('title', 'text', 'image')


class DiscussionForm(forms.ModelForm):

    class Meta:
        model = Discussions
        fields = ('title', 'text', 'tags')


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('title', 'image', 'main_genre', 'add_genre_1', 'add_genre_2', 'tags', 'age18', 'price', 'ended')


class ChapterForm(forms.ModelForm):

    class Meta:
        model = BookChapter
        fields = ('title', 'image', 'text', 'posted')


class ProfileForm(forms.Form):
    nickname = forms.CharField(label='nickname', max_length=50, required=True)
    profile_picture = forms.ImageField(label='profile_picture', required=False)


class SignupForm(forms.Form):
    nickname = forms.CharField(label='nickname', max_length=50, required=True)
    profile_picture = forms.ImageField(label='profile_picture', required=True)

    def signup(self, request, user):
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.nickname = request.POST['nickname']
        user.save()
        user_profile.save()
