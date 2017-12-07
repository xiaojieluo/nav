from mongoengine import Document, StringField, IntField
from nav.model import Model

class User(Document, Model):
    username = StringField(require = True, unique = True)
    password = StringField()
    age = IntField()

    @classmethod
    def login(cls, *args, **kw):
        '''
        user login
        '''
        data = dict(
            username = kw.get('username', None),
            password = kw.get('password', None)
        )
        user = cls.objects(**data).first()

        return user

    @classmethod
    def register(cls, *args, **kw):
        '''user register'''
        # 过滤 model 中未定义的 fields
        data = {k:v for k, v in kw.items() if k in cls._fields }
        user = cls(**data)
        user.save()
