from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widget = {
            'text':
            forms.Textarea(attrs={'rows':3,'placeholder':'نظر خود رو بنویسید...'})
        }