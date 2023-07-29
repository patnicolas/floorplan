import json
from typing import AnyStr, List


class SerializableClass(object):
    def get_args(self) -> List[AnyStr]:
        pass

    def build(self, args: List[AnyStr]):
        pass


class TSerializable(object):
    def __init__(self, serializable_class: SerializableClass):
        self.serializable_class = serializable_class

    def serialize(self) -> AnyStr:
        args = self.serializable_class.get_args()
        return json.dumps({'class': self.__class__.__name__, 'args': args})

    def __str__(self):
        params = self.serializable_class.get_args()
        return str(params)


class TDeserializable(TSerializable):

    def deserializable(self, json_data: AnyStr) -> SerializableClass:
        params = json.loads(json_data)
        self.serializable_class.build(params['args'])
        return self.serializable_class
