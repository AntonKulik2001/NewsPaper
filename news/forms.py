from django import forms
from django.core.exceptions import ValidationError

from .models import *

class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=[
            'author',
            'postCategory',
            'title',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if text[0].islower():
            raise ValidationError(
                "Текст должно начинаться с заглавной буквы"
            )

        if title[0].islower():
            raise ValidationError(
                "Заголовок должно начинаться с заглавной буквы"
            )

        return cleaned_data