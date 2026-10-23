from django import forms
from .models import Post,Comment
from tinymce.widgets import TinyMCE

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widget = {
            'text':
            forms.Textarea(attrs={'rows':3,'placeholder':'نظر خود رو بنویسید...'})
        }
        labels = {'text':'متن'}

class PostAdminForm(forms.ModelForm):
    text = forms.CharField( widget=TinyMCE(
            attrs={
                'cols': 80,
                'rows': 30,
            },
            mce_attrs={
                'height': 450,
                'directionality': 'rtl',
                'language': 'fa',
                'plugins': 'lists link table code',
                'toolbar': (
                    'undo redo | blocks | bold italic | '
                    'alignleft aligncenter alignright alignjustify | '
                    'bullist numlist | link table | code'
                ),
            },
        )
    )

    class Meta:
        model = Post
        fields = '__all__'