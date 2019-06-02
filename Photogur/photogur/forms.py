from django.forms import Form, CharField, PasswordInput, ModelForm
from .models import Picture

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['title', 'artist', 'url']

