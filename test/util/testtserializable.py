

from unittest import TestCase
from typing import AnyStr, List
from src.util.tserializable import TSerializable, TDeserializable, SerializableClass



class TestTSerializable(TestCase):
    def test_serialize(self):

        class MyEntry(SerializableClass):
            def __init__(self, name: AnyStr = '', position: AnyStr = ''):
                self.name = name
                self.position = position

            def get_args(self) -> List[AnyStr]:
                return [self.name, self.position]

            def build(self, args: List[AnyStr]):
                print(args)
                self.name = 'hello'
                self.name = args[0]
                self.position = args[1]

            def __str__(self):
                return f'Name: {self.name} ,Position: {self.position}'

        myEntry = MyEntry("Dolly", "Singer")
        tSerializable = TSerializable(myEntry)
        json_dump = tSerializable.serialize()
        print(json_dump)
        tDeserializable = TDeserializable(MyEntry())
        new_entry = tDeserializable.deserializable(json_dump)
        print(str(new_entry))





