from django import forms


class PostUrlForm(forms.Form):
    class Meta:
        fields = forms.URLField(help_text='올바른 url 주소를 입력하세요')
