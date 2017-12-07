from mongoengine import Document, StringField, ListField, DateTimeField
import datetime
from nav.model import Model

class Link(Document, Model):
    uid = StringField(require = True)
    username = StringField(require = True)
    url = StringField(require = True)
    title = StringField(require = True)
    tags = ListField(StringField())
    published_at = DateTimeField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    @classmethod
    def add(cls, *args, **kw):
        '''
        add a new link in mongodb
        '''
        data = {k:v for k, v in kw.items() if k in cls._fields }
        # 更新一些其余的数据
        data.update({
            'tags': data.get('tags', '').split(','),
            'created_at': datetime.datetime.now(),
            'published_at': datetime.datetime.now()
        })
        link = cls(**data)
        link.save()

    def update(self, **kw):
        '''
        更新操作
        转换tags 为 列表
        '''
        kw.update({
            # 将字符串值根据,分割成列表， 并且清除列表元素两边的空格
            'tags': [ t.strip() for t in kw.get('tags', '').split(',') ],
            'updated_at': datetime.datetime.now(),
        })
        print(kw)
        return super().update(**kw)
