import dateutil.rrule as rrule
from django import forms
#import widgets
from django.utils.translation import ugettext_lazy as _


class RRuleWidget(forms.MultiWidget):
    """
    A widget that splits rrule input into ...
    """
    def __init__(self, choices=None):
        widgets = (
                forms.DateTimeInput(),
                forms.Select(choices=choices)
                )
        super(RRuleWidget, self).__init__(widgets)

    def decompress(self, value):
        if value:
            return [value._dtstart, value._freq]
        return [None, None]


class RRuleField(forms.MultiValueField):
    choices=list(enumerate(
        ('YEARLY', 'MONTHLY', 'WEEKLY',
            'DAILY', 'HOURLY', 'SECONDLY')))
    widget = RRuleWidget(choices)

    def __init__(self, *args, **kwargs):
        fields = (
                forms.DateTimeField(
                    label='start datetime'
                    ),
                forms.ChoiceField(
                    choices=self.choices,
                    label='frequency'
                    ),
                )
        super(RRuleField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        print data_list
        if data_list:
            return rrule.rrule(freq=data_list[1], count=1, dtstart=data_list[0])
        return None
