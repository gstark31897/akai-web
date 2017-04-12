from mongoengine import *

from ..model.user import User


class Message(Document):
    content = StringField(required=True)
    sender = ObjectIdField(required=True)
    receiver = ObjectIdField()
    group = ObjectIdField()

    @staticmethod
    def get_messages(user):
        return Message.objects(sender=user.id, receiver__in=[user.id])

    @staticmethod
    def create(content, sender, receiver):
        return Message(content=content, sender=sender, receiver=receiver).save()
        

    @staticmethod
    def send_message(content, sender, receiver_name):
        receiver = User.get_user(receiver_name)
        Message.create(content, sender.id, receiver.id)
        

    @property
    def sender_name(self):
        return User.get_user_by_id(self.sender).username

