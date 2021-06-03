import warnings

import pytest


def deprecated(since, message):
    def do_warn(cls):
        warnings.warn(
            f"{cls.__name__}: {message}, {since}", DeprecationWarning,
        )

    class DeprecationMeta(type):
        def __new__(mcs, name, bases, namespace):
            new_cls = super().__new__(mcs, name, bases, namespace)
            origin_init = new_cls.__init__

            def __init__(self, *args, **kwargs):
                origin_init(self, *args, **kwargs)
                do_warn(type(self))

            setattr(new_cls, "__init__", __init__)
            return new_cls

    def wrapper(cls):
        class WrappedCls(cls, metaclass=DeprecationMeta):
            pass

        WrappedCls.__name__ = cls.__name__
        WrappedCls.__doc__ = cls.__doc__
        WrappedCls.__module__ = cls.__module__
        return WrappedCls

    return wrapper


@deprecated(since="2020-09-01", message="Deprecated functionality")
class Base:
    def __init__(self, *args, **kwargs):
        print("Inside Base")


class Child(Base):
    def __init__(self, *args, **kwargs):
        print("Inside Child")
        super().__init__(*args, **kwargs)


class ChildOfChild(Child):
    def __init__(self, *args, **kwargs):
        print("Inside ChildofChild")
        super().__init__(*args, **kwargs)


def test_child_knows_its_base():
    with pytest.deprecated_call(
        match="Base: Deprecated functionality, 2020-09-01"
    ):
        Base()
    with pytest.deprecated_call(
        match="Child: Deprecated functionality, 2020-09-01"
    ):
        Child()
    with pytest.deprecated_call(
        match="ChildOfChild: Deprecated functionality, 2020-09-01"
    ):
        ChildOfChild()
