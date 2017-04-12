from mongoengine import *

import hashlib, binascii, os


def gen_salt():
    return binascii.hexlify(os.urandom(64)).decode('utf-8')


def hash_password(password, salt, iterations=10000):
    password = password.encode('utf-8')
    salt = salt.encode('utf-8')
    for i in range(iterations):
        password = hashlib.sha512(password + salt).hexdigest().encode('utf-8')
    return password.decode('utf-8')


class User(Document):
    username = StringField(required=True, unique=True)
    salt = StringField(required=True)
    password = StringField(required=True)
    friends = ListField(ObjectIdField(), default=[])
    is_authenticated = BooleanField(default=False)
    is_active = BooleanField(default=False)
    is_anonymous = BooleanField(default=False)

    @staticmethod
    def get_user(username):
        for user in User.objects(username=username):
            return user
        return None

    def get_id(self):
        return self.username

    def login(self, password):
        if hash_password(password, self.salt) == self.password:
            self.is_authenticated = True
            self.is_active = True
        else:
            self.is_authenticated = False
            self.is_active = False
        self.save()

    @staticmethod
    def create(username, password):
        salt = gen_salt()
        password = hash_password(password, salt)
        return User(username=username, salt=salt, password=password).save()

