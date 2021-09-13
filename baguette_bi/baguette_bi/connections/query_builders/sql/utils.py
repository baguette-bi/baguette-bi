def just_fn(name):
    return staticmethod(lambda x: f'{name}("{x}")')


class NotImplementedSQLFunction:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner=None):
        raise NotImplementedError(
            f"SQL function {self.name} is not supported by {instance.__class__.__name__}"
        )

    def __set__(self, instance, value):
        raise AttributeError
