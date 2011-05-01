from django import forms

class RRuleWidget(forms.MultiWidget):

    input_formats = forms.DateTimeInput.format

    def __init__(self, attrs=None, input_formats=None):
        widgets = (forms.DateTimeInput(attrs=attrs, format=input_formats),
                )
        super(RRuleWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value is None:
            return [None,]
        return [value._dtstart,]
