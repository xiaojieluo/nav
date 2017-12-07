class Model(object):

    def update(self, **kw):
        print("This is Model's update")

class User(Model):

    def update(self, **kw):
        print("Hello, User Model.")
        return super().update(**kw)

if __name__ == '__main__':
    u = User()
    u.update()
