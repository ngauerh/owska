from .models import *


def message_tips(**kwargs):
    MessageTips.objects.create(topic_id=kwargs['topic'], sender_id=kwargs['sender'], receiver_id=kwargs['receiver'],
                                   tips_action=kwargs['tips_action'], tips_content=kwargs['tips_content'])
