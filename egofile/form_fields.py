from django import forms
from widgets import SingleImageWidget, MultiImageWidget

class SingleImageFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = SingleImageWidget
        super(SingleImageFormField, self).__init__(*args, **kwargs)

class MultiImageFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = MultiImageWidget
        super(MultiImageFormField, self).__init__(*args, **kwargs)

