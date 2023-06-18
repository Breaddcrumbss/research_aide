from django import forms


class SearchForm(forms.Form):
    input = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 150}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['input'].label = ""