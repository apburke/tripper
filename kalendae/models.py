from django.db import models
from fields import RRuleField

class Calendar(models.Model):
    """
    Details of a specific calendar
    """
    #fields
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("calendar_view", [str(self.id)])

class Event(models.Model):
    """
    Details of an event
    """
    #fields
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    parent = models.ForeignKey("self", null=True, blank=True)

    def __unicode__(self):
        return self.name

class Session(models.Model):
    """
    Details of an event's session
    """
    event = models.ForeignKey(Event)
    rrule = RRuleField(null=True)

    def __unicode__(self):
        return "Session for {0}".format(unicode(self.event))
