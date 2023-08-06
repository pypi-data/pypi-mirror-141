# Imports
from dataclasses import dataclass
from typing import Union, Any, Optional, Set
import unittest

from mooss.serialize.interface import ISerializable
from mooss.serialize._field_types import EFieldType


# Classes
@dataclass
class TestedValidClass(ISerializable):
    pass


class GenericClass:
    pass


# Unit tests
class TestTypeAnalysis(unittest.TestCase):
    def test_all(self):
        """
        Testing if validly types are properly detected.
        """
        
        print("Testing valid primitive types...")
        self.assertEqual((True, EFieldType.FIELD_TYPE_PRIMITIVE), ISerializable._analyse_type(int, int))
        self.assertEqual((True, EFieldType.FIELD_TYPE_PRIMITIVE), ISerializable._analyse_type(str, str))
        self.assertEqual((True, EFieldType.FIELD_TYPE_PRIMITIVE), ISerializable._analyse_type(float, float))
        self.assertEqual((True, EFieldType.FIELD_TYPE_PRIMITIVE), ISerializable._analyse_type(bool, bool))
        
        print("Testing valid list, dict, tuple, set...")
        self.assertEqual((True, EFieldType.FIELD_TYPE_ITERABLE), ISerializable._analyse_type(list, list))
        self.assertEqual((True, EFieldType.FIELD_TYPE_ITERABLE), ISerializable._analyse_type(dict, dict))
        self.assertEqual((True, EFieldType.FIELD_TYPE_ITERABLE), ISerializable._analyse_type(tuple, tuple))
        self.assertEqual((True, EFieldType.FIELD_TYPE_ITERABLE), ISerializable._analyse_type(set, set))
        
        print("Testing valid composed list, dict, tuple, set...")
        self.assertEqual((True, EFieldType.FIELD_TYPE_ITERABLE),
                         ISerializable._analyse_type(list[str, int], type(["abc"])))
        self.assertEqual((True, EFieldType.FIELD_TYPE_ITERABLE),
                         ISerializable._analyse_type(dict[str, int], type({'text': 'test', 'number': 123})))
        self.assertEqual((True, EFieldType.FIELD_TYPE_ITERABLE),
                         ISerializable._analyse_type(tuple[str, int], type(("abc",))))
        # FIXME: self.assertEqual((True, None)ISerializable.is_type_valid(set[str, int], list))
        
        print("Testing valid individual types in list...")
        self.assertEqual((True, EFieldType.FIELD_TYPE_PRIMITIVE),
                         ISerializable._analyse_type([str, int], int, process_listed_types=True))
        
        print("Testing valid serializable class...")
        self.assertEqual((True, EFieldType.FIELD_TYPE_SERIALIZABLE),
                         ISerializable._analyse_type(TestedValidClass, dict))
        
        print("Testing valid typing special types...")
        self.assertEqual((True, EFieldType.FIELD_TYPE_PRIMITIVE), ISerializable._analyse_type(Union[str, int], int))
        self.assertEqual((True, EFieldType.FIELD_TYPE_PRIMITIVE), ISerializable._analyse_type(Optional[str], str))
        self.assertEqual((True, EFieldType.FIELD_TYPE_PRIMITIVE), ISerializable._analyse_type(Optional[str], None))
        self.assertEqual((True, EFieldType.FIELD_TYPE_PRIMITIVE), ISerializable._analyse_type(None, None))
        
        print("Testing validity with 'Any'...")
        for tested_type in [int, str, float, bool, [str, int]]:
            self.assertEqual((True, EFieldType.FIELD_TYPE_UNKNOWN),
                             ISerializable._analyse_type(Any, tested_type, process_listed_types=True))
        
        print("Testing the absence of 'TypeError' with 'Any' and list of individual types...")
        self.assertEqual((True, EFieldType.FIELD_TYPE_UNKNOWN),
                         ISerializable._analyse_type(Any, int, process_listed_types=False))
    
    def test_invalid_special_exceptions(self):
        """
        Testing some specific exceptions that may be handled differently later on.
        """
        
        print("Testing is a 'TypeError' is raise with unknown classes...")
        # Testing with 'GenericClass' since they are not supported yet and should trigger this specific exception.
        try:
            ISerializable._analyse_type(GenericClass, int)
        except TypeError as err:
            self.assertTrue("nor is it a class !" in str(err))
        
        print("Testing is a 'TypeError' is raise with unknown types...")
        # Testing with a 'Set' since they are not supported yet and should trigger this exception.
        try:
            ISerializable._analyse_type(Set, int)
        except TypeError as err:
            self.assertTrue("is not supported by 'ISerializable' !" in str(err))


# Main
if __name__ == '__main__':
    unittest.main()
