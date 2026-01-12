from django import forms
from . import models as home_models


class PictureForm(forms.ModelForm):
    delete_password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=4,
        max_length=18,
        help_text='Required to delete the image early'
    )

    class Meta:
        model = home_models.Picture
        fields = ('image',)

    def save(self, commit=True):
        picture = super().save(commit=False)
        picture.set_password(self.cleaned_data['delete_password'])
        if commit:
            picture.save()
        return picture


class DeletePictureForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput,
        max_length=18,
        label='Deletion Password'
    )
