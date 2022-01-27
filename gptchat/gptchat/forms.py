from django import forms

class BotForm(forms.ModelForm):
    class Meta:
        fields = ("message",)
