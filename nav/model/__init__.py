from mongoengine import connect, QuerySet
import copy
connect('nav')


class Model(object):

    @classmethod
    def find_all(cls, conditions = None, sort = None, fields = None, limit = None, skip = 0, **kw):
        '''
        查找指定的数据
        Args:
            conditions -> dict()
            kw -> dict() 输入的键值对条件
            可以用两种方式来传递参数， 一种是字典式， 一种是键值对式
        '''
        if conditions is None:
            conditions = {}
        if kw is not None:
            conditions.update(kw)

        data =  cls.objects(**conditions) \
                    .order_by(sort) \
                    .limit(limit) \
                    .skip(skip)

        # 处理数据， 添加一个字段： objectid ， 表示 str 类型的 objectid
        # result = QuerySet()
        # if data is not None:
        #     for d in data:
        #         d.objectid = str(d.id)
        #         result.append(d)

        return data

    @classmethod
    def find(cls, conditions = None, sort = None, fields = None, **kw):
        '''
        返回一条数据， 其他用法和 find_all 一致
        '''
        if conditions is None:
            conditions = {}
        if kw is not None:
            conditions.update(kw)

        data = cls.find_all(conditions = conditions, sort = sort, fields = fields, limit = 1, skip = 0)

        if data:
            return data.first()

        return None

    # @classmethod
    # def update(cls, *args, **kw):
    #     '''更新数据'''
    #


# loading model
from .user_model import User
from .link_model import Link
