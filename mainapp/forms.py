from django import forms
from models import SiteMessages

class SiteMessagesForm(forms.ModelForm):
    class Meta:
        model = SiteMessages
        fields =['username', 'email', 'topic', 'message']