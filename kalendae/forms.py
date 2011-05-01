from dateutil.rrule import *
from django import forms
import  widgets
from django.utils.translation import ugettext_lazy as _

class RRuleField(forms.MultiValueField):
    widget = widgets.RRuleWidget

    def __init__(self, input_formats=None, *args,
            **kwargs):
        fields = (
                forms.DateTimeField(input_formats=input_formats),
                )
        super(RRuleField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        print data_list
        if data_list:
            return rrule(0, count=1, dtstart=data_list[0])
        return None

class RecurringDateTimeWidget(forms.SplitDateTimeWidget):
    """
    A widget that splits rrule input into ...
    """
    def __init__(self, attrs=None, date_format=None, time_format=None):
        super(RecurringDateTimeWidget, self).__init__(attrs, date_format,
                time_format)

    def decompress(self, value):
        if value:
            return super(RecurringDateTimeWidget, self).decompress(value._dtstart)
        return None

class RecurringDateTimeField(forms.MultiValueField):
    widget = forms.SplitDateTimeWidget

    def __init__(self, input_date_formats=None, input_time_formats=None, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)
        fields = (
                SplitDateTimeField(input_date_formats=input_date_formats,
                    input_time_formats=input_time_formats),

                )
        super(RecurringDateTimeField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            pass
        return None
