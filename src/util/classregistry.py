import json
import logging


class ClassRegistry(object):
    def __init__(self):
        self.registry = {}

    def register(self, target_class: type):
        self.registry[target_class.__name__] = target_class

    def unregister(self, target_class: type):
        try:
            del self.registry[target_class.__name__]
        except Exception as e:
            logging.error(e)


class Meta(type):
    registry = ClassRegistry()

    def __new__(meta, name, bases, class_dict) -> Meta:
        cls = type.__new__(meta, name, bases, class_dict)
        Meta.registry.register(cls)
        return cls

