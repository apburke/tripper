import datetime
from dateutil import rrule
from django.db import models
from django.core import validators
import forms
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
import re
import ast

# Until form is done, override rrule's unicode method to be descriptive enough
# to rebuild the object
rrule_kwargs = ('freq', 'dtstart', 'interval', 'wkst', 'count', 'until',
    'bysetpos', 'bymonth', 'bymonthday', 'byyearday', 'byeaster', 'byweekno',
    'byweekday', 'byhour', 'byminute', 'bysecond')
setattr(rrule.rrule, 'kwargs', rrule_kwargs)

def rrule_unicode(self):
    prep_value = str()
    for k in self.kwargs:
        v = getattr(self, "_"+k)
        if v is not None:
            prep_value += "{0}={1};".format(k, v)
    return prep_value
setattr(rrule.rrule, '__unicode__', rrule_unicode)


class TimeDeltaField(models.Field):
    description = _("TimeDelta")
    timedelta_regex = re.compile(r"""^(?:(?P<days>-?\d{1,9})\ days,\ )?
                                     (?P<hours>\d{1,2}):
                                     (?P<minutes>\d{2}):
                                     (?P<seconds>\d{2}(?:\.\d{6})?)$""", re.X)
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "CharField"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 32
        super(TimeDeltaField, self).__init__(*args, **kwargs)
        self.validators.append(validators.RegexValidator(self.timedelta_regex))

    def get_prep_value(self, value):
        if isinstance(value, basestring) or value is None:
            return value
        return unicode(value)

    def to_python(self, value):
        if isinstance(value, datetime.timedelta) or value is None:
            return value
        if value == '':
            return None
        #kwargs = self.timedelta_regex.match(value).groupdict(0)
        kwargs = dict([(k, ast.literal_eval(v) ) for (k, v) in
            self.timedelta_regex.match(value).groupdict('0').iteritems()])
        return datetime.timedelta(**kwargs)


class RRuleField(models.Field):
    description = _("Recurrence rule")
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        super(RRuleField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def get_prep_value(self, value):
        if isinstance(value, basestring) or value is None:
            return value
        return unicode(value)

    def to_python(self, value):
        if isinstance(value, rrule.rrule) or value is None:
            return value
        if value == '':
            return None
        kwargs = dict()
        for kv in value.split(";")[:-1]:
            k,v = kv.split("=")
            if k == "dtstart" or k == "until":
                kwargs[k] = datetime.datetime.strptime(v,
                    "%Y-%m-%d %H:%M:%S")
            else:
                kwargs[k] = ast.literal_eval(v)
        return rrule.rrule(**kwargs)

    def value_to_string(self, obj):
        assert(False)

