import threading

lock = threading.Lock()


class ParametricSingleton(type):
    """
    This class acts as a metaclass and ensures
    that only one instance of object class is
    created for same set of arguments passed.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        instance_key = str(cls.__name__)
        for arg in args:
            instance_key = instance_key + "_" + arg
        for key, val in kwargs.items():
            instance_key = instance_key + "_" + val
        if instance_key not in cls._instances:
            with lock:
                if instance_key not in cls._instances:
                    cls._instances[instance_key] = super(
                        ParametricSingleton, cls
                    ).__call__(*args, **kwargs)
        return cls._instances[instance_key]
