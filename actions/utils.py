from .models import Action
from django.utils import timezone
import datetime
from django.contrib.contenttypes.models import ContentType


def create_action(user,verb,content_object=None):
    currenttime=timezone.now()
    last_minute=currenttime-datetime.timedelta(minutes=1)
    actions=Action.objects.filter(user_id=user.id,verb=verb,created__gte=last_minute)
    print(actions,"actions")
    print(content_object,"content_object")
    if content_object:
        content_type=ContentType.objects.get_for_model(content_object)
        similar_actions=actions.filter(content_type=content_type,object_id=content_object.id)
        print(content_type,"content_type")
        print(similar_actions,"similar_actions")
    if not similar_actions:
        action=Action(user=user,verb=verb,content_object=content_object)
        action.save()
        return True
    return False

