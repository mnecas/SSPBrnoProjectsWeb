from django import template

from ..models import Anketa, Event, User

register = template.Library()


def rated(user_id, event_id):
    user = User.objects.filter(id=user_id).first()
    event = Event.objects.filter(id=event_id).first()
    if Anketa.objects.filter(user=user, event=event):
        return True
    return False


register.filter(rated)
