from django import forms
from django.forms import ModelForm

from .models import InboxMessage


class InboxNewMessageForm(ModelForm):
    class Meta:
        model = InboxMessage
        fields = ['body']
        labels = {
            'body': ''
        }
        widgets = {

            'body': forms.Textarea(attrs={'rows': 4,
                                          'placeholder': 'Add message ...', 'class': 'w-full p-3 bg-green-50 text-black rounded-xl border border-gray-300 focus:outline-none focus:ring-2 '
                                                                                     'focus:ring-blue-500',
                                          }),
        }
