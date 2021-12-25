from django import forms


class CreateNewPage(forms.Form):
    """ Form to create new entry """
    
    title = forms.CharField(label = 'Title', max_length = 50, required = True,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
    )
    textarea = forms.CharField(required = True, widget = forms.Textarea(attrs={'class': 'form-control'}), label = '')