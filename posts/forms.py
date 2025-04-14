from django import forms
from django.forms import ModelForm

from posts.models import *


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['author', 'likes']
        labels = {
            'body': 'Caption',
            'tags': 'Category',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption...', 'class': 'font1 text-4xl'}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'tags']
        labels = {
            'body': '',
            'tags': 'Category',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'class': 'font1 text-4xl'}),
            'tags': forms.CheckboxSelectMultiple(),

        }


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Add Comment ...'})
        }
        labels = {
            'body': ''
        }


class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Add Reply ...',
                'class': "!text-sm"
            })
        }
        labels = {
            'body': ''
        }
