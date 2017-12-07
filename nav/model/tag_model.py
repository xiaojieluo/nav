from mongoengine import Document, StringField
from nav.model import Model

class Tag(Document, Model):
    name = StringField()
