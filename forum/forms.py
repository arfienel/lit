from django import forms
from .models import *

# author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# title = models.CharField('Заголовок', max_length=200)
# text = models.TextField('текст новости')
# pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
# image = models.ImageField('изображение', upload_to='photos/%y/%m/%d/')
# likes = models.ManyToManyField(User, related_name='news_likes', blank=True)


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
        fields = ('title', 'book_author', 'image', 'text_example', 'tags', 'age18', 'price', 'ongoing')


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
        user.save()
        user_profile.save()
