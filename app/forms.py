from django import forms


class SearchForm(forms.Form):
    input = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control", 'placeholder': "Describe your case..."}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['input'].label = ""