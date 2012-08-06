from django.db import models
from form_fields import SingleImageFormField, MultiImageFormField

class SingleImageField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 200
        super(SingleImageField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = SingleImageFormField
        return super(SingleImageField, self).formfield(**kwargs)

class MultiImageField(models.TextField):

    def formfield(self, **kwargs):
        kwargs['form_class'] = MultiImageFormField
        return super(MultiImageField, self).formfield(**kwargs)

