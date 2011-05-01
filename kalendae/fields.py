import datetime
from dateutil.rrule import *
from django.db import models
import forms
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

def rrule_unicode(self):
    kargs = ('freq', 'dtstart', 'interval', 'wkst', 'count', 'until',
    'bysetpos', 'bymonth', 'bymonthday', 'byyearday', 'byeaster', 'byweekno',
    'byweekday', 'byhour', 'byminute', 'bysecond')
    value = unicode()
    for k in kargs:
       v = getattr(self, "_{0}".format(k))
       if v is not None:
           value = "{0}{1}={2}\n".format(value, k, repr(v))
    return value.strip()
setattr(rrule, '__unicode__', rrule_unicode)

class RRuleField(models.Field):
    description = _("Recurrence rule (for date/datetimes)")
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "TextField"

    def get_prep_value(self, value):
        if isinstance(value, basestring) or value is None:
            return value
        return smart_unicode(value)

    def to_python(self, value):
        if isinstance(value, rrule) or value is None:
            return value
        kargs = dict()
        for karg in value.split("\n"):
            k,v = karg.split('=')
            kargs[k] = eval(v)
        return rrule(**kargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.RRuleField}
        defaults.update(kwargs)
        return super(RRuleField, self).formfield(**defaults)
