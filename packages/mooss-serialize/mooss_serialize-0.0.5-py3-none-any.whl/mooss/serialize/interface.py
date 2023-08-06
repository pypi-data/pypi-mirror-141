# Imports
from abc import ABC
import copy
from dataclasses import Field, MISSING
import json
from typing import Union, get_origin, get_args, Any, Optional

from ._field_types import EFieldType


# Classes
class ISerializable(ABC):
    """
    Interface that provides a couple of methods to easily serialize and deserialize classes to and from dictionaries.
    """
    
    __dataclass_fields__: dict[str, Field]
    """
    Reference to the hidden field added to classes by the @dataclass decorator to prevent PyCharm from throwing a fit
    when using this field.
    """
    
    # FIXME: Add check to see if the class is properly decorated !
    
    @classmethod
    def _get_serializable_fields(cls) -> dict[str, Field]:
        """
        Get a dict of all the serializable variables and their types.
        
        :return: A dictionary containing all the serializable variables with the variable as the key, and
        a 'Field' object from the 'dataclasses' module representing them.
        """
        
        # TODO: Add a way to filter out fields when declaring the class !
        
        return cls.__dataclass_fields__
    
    @classmethod
    def _is_field_serializable(cls, field_name) -> bool:
        """
        Check if a given field is serializable.
        
        :param field_name: Field's name to check.
        :return: True if it is serializable, False otherwise.
        """
        
        return field_name in cls._get_serializable_fields()
    
    @classmethod
    def _get_field_definition(cls, field_name) -> Optional[Field]:
        """
        Gets a given field's 'Field' definition.
        
        :param field_name: Field's name to check.
        :return: The relevant 'Field' object if found, None otherwise.
        """
        
        return cls._get_serializable_fields().get(field_name)
    
    @classmethod
    def _analyse_type(cls, expected_type, actual_type, process_listed_types: bool = False) -> tuple[bool, EFieldType]:
        """
        Analyses a given type and checks the given types are compatible and which type of field it is.
        
        The 'expected_type' parameter should be the class' annotations' types.
        
        :param expected_type: The expected type against which 'actual_type' will be compared.
        :param actual_type: The type of the data to be deserialized which will be compared against 'expected_type'.
        :param process_listed_types: Performs a recursive check on types given in a list.  (Not list with arguments !)
        :return: True if the type is valid and compatible, False otherwise.
        :raises TypeError: If one of the given type is not supported internally.
        """
        
        # print("> is_type_valid: '{}', '{}'".format(expected_type, actual_type))
        
        # Fixing some potential issues
        if expected_type is None:
            # print(">> Fixing 'expected_type' from 'None' to 'NoneType' !")
            expected_type = type(None)
        
        if actual_type is None:
            # print(">> Fixing 'actual_type' from 'None' to 'NoneType' !")
            actual_type = type(None)
        
        # Testing some basic stuff
        if expected_type == type(None):
            # print(">> Found 'NoneType' !")
            # print(">> {} == {} -> {}".format(expected_type, actual_type, expected_type == actual_type))
            return expected_type == actual_type, EFieldType.FIELD_TYPE_PRIMITIVE
        
        if expected_type is Any:
            return True, EFieldType.FIELD_TYPE_UNKNOWN
        
        if expected_type in [str, int, bool, float]:
            # print(">> Detected a primitive type, not performing any filtering !")
            return expected_type is actual_type, EFieldType.FIELD_TYPE_PRIMITIVE
        elif get_origin(expected_type) is Union:
            # print(">> Detected a 'Union' or 'Optional' type")
            for individual_expected_type in get_args(expected_type):
                # print(">> Testing '{}'...".format(individual_expected_type))
                analysed_data_result = cls._analyse_type(expected_type=individual_expected_type,
                                                         actual_type=actual_type,
                                                         process_listed_types=process_listed_types)
                # print(">> Found a valid match for the union/optional !")
                if analysed_data_result[0]:
                    return analysed_data_result
        elif isinstance(expected_type, type):
            # print(">> Detected a 'type' type '{}'".format(expected_type))
            # print(">> origin:'{}' & args:'{}'".format(get_origin(expected_type), get_args(expected_type)))
            # Catches classes, list, list[a, b], ...
            
            # TODO: Check if the following can be supported:
            #  Set, collection, namedTuple, NewType, Mapping, Sequence, Sequence, TypeVar, Iterable
            
            # Testing for composed types
            if get_origin(expected_type) in [list, dict, tuple, set]:
                # print(">> Encountered a composed type -> {}".format(get_args(expected_type)))
                expected_type = get_origin(expected_type)
            
            # Checking for composed types and classes
            if expected_type in [list, dict, tuple, set]:
                # Simple list/dict/tuple
                # print(">> Simple list/dict/tuple")
                return expected_type is actual_type, EFieldType.FIELD_TYPE_ITERABLE
            
            # Checking for ISerializable interfaces
            # This check is disgusting, but it fixes the following error with list, dict, ???:
            # |_> TypeError: issubclass() arg 1 must be a class
            if expected_type.__class__ is not type:
                # print(">> Should be a class a class -> '{}' !".format(expected_type.__class__))
                # print(">> Does implement ISerializable ? -> {}".format(issubclass(expected_type, ISerializable)))
                # print(">> Is actual_type a dict ? -> {}".format(actual_type is dict))
                # TODO: Check for null !
                return issubclass(expected_type, ISerializable) and actual_type is dict,\
                       EFieldType.FIELD_TYPE_SERIALIZABLE
            else:
                # print(">> Not a class or None !")
                raise TypeError("The expected type '{}' is a type that is not supported, nor is it a class !".format(
                    expected_type
                ))
        
        elif isinstance(expected_type, list):
            # Only gets triggered when passing list of individual types, not complex lists such as 'list[a, b]' !
            if process_listed_types:
                for individual_expected_type in expected_type:
                    analysed_data_result = cls._analyse_type(expected_type=individual_expected_type,
                                                             actual_type=actual_type,
                                                             process_listed_types=process_listed_types)
                    if analysed_data_result[0]:
                        return analysed_data_result
            else:
                raise TypeError("The expected type '{}' is a list of individual types !")
        else:
            # print(">> WTF !!!")
            raise TypeError("The expected type '{}' is not supported by 'ISerializable' !".format(expected_type))
        
        # Default return case when encountering supported types.
        return False, EFieldType.FIELD_TYPE_UNKNOWN

    @classmethod
    def _is_type_valid(cls, expected_type, actual_type, process_listed_types: bool = False) -> bool:
        """
        Checks if a given type is the same or contained within a given set or expected types.
        
        The 'expected_type' parameter should be the class' annotations' types.
        
        :param expected_type: The expected type against which 'actual_type' will be compared.
        :param actual_type: The type of the data to be deserialized which will be compared against 'expected_type'.
        :param process_listed_types: Performs a recursive check on types given in a list.  (Not list with arguments !)
        :return: True if the type is valid and compatible, False otherwise.
        :raises TypeError: If one of the given type is not supported internally.
        """
        
        return cls._analyse_type(expected_type, actual_type, process_listed_types)[0]
    
    @classmethod
    def from_dict(cls, data_dict: dict, allow_unknown: bool = False, add_unknown_as_is: bool = False,
                  allow_as_is_unknown_overloading: bool = False, allow_missing_required: bool = False,
                  allow_missing_nullable: bool = True, add_unserializable_as_dict: bool = False,
                  validate_type: bool = True, parsing_depth: int = -1, do_deep_copy: bool = False):
        """
        Deserialize a given dict into the relevant serializable class.
        
        :param data_dict: Dictionary containing the data to deserialize.
        :param allow_unknown: Allow unknown fields to be processed, other parameters will determine their use if 'True'.
        :param add_unknown_as_is: Adds unknown fields/values as-is in the final class if 'allow_unknown' is also 'True'.
        :param allow_as_is_unknown_overloading: Allow unknown fields/values to overload existing class attributes.
        :param allow_missing_required: ! Not used yet !
        :param allow_missing_nullable: ! Not used yet !
        :param add_unserializable_as_dict: ! Not used yet !
        :param validate_type: Enables a strict type check between the class' serializable fields and the given data.
        :param parsing_depth: The recursive depth to which the deserialization process will go.  (-1 means infinite)
        :param do_deep_copy: Performs a deep copy of the given 'data_dict' to prevent modifications from affecting
        other variables that may reference it.
        :return: The parsed 'ISerializable' class.
        :raises TypeError: If a mismatch between the expected and received data's types is found, requires
         'validate_type' to be set to 'True'.
        :raises ValueError: If an unknown field is given and cannot be allowed or added back in the final class.
        """
        
        # TODO: Maybe -> allow_primitive_type_casting: bool
        
        # TODO: Explicitly test 'do_deep_copy'
        
        # FIXME: Check for missing required fields, or let the interpreter do it during instantiation ?
        
        # print("> from_dict: '{}', '{}'".format(data_dict, allow_unknown))
        
        # Checking if we have reached the end of the allowed recursive depth.
        if parsing_depth == 0:
            # print(">> Returning early due to recursive depth. !")
            return data_dict
        
        # Checking for unknown fields.
        _temp_data_dict: dict[str, Any] = dict()
        """
        Internal dictionary used to store a copy of the fields being analysed, processed and modified in order to avoid
        changing values in the potentially referenced 'data_dict' value.
        """
        
        _unknown_data: Optional[dict[str, Any]] = dict() if allow_unknown and add_unknown_as_is else None
        """
        Nullable dictionary that may exist and contain any unknown field that will be handled when instantiating the
        'ISerializable' class itself.
        May be left as 'None' if it shouldn't be used !
        """
        
        for field_name, field_value in data_dict.items():
            # print(">> Checking what to do with '{}'...".format(field_name))
            if not cls._is_field_serializable(field_name):
                if allow_unknown:
                    if add_unknown_as_is:
                        # print(">> Separating")
                        # Separating this field into '_unknown_data' for later.
                        _unknown_data[field_name] = copy.deepcopy(field_value) \
                            if do_deep_copy else copy.copy(field_value)
                    else:
                        # print(">> Removing by ignoring it")
                        # Ignoring this field safely by not copying it in the '_temp_data_dict' dict.
                        pass
                else:
                    # print(">> Raising error")
                    # Not allowing any.
                    raise ValueError("The field '{}' is not present in the '{}' class !".format(
                        field_name, cls.__name__))
            else:
                # print(">> Copying")
                # Copying any other valid fields as-is.
                _temp_data_dict[field_name] = copy.deepcopy(field_value) \
                    if do_deep_copy else copy.copy(field_value)
        
        # Analysing all valid fields before using them to instantiate a new 'ISerializable' class.
        for expected_field_name, expected_field_definition in cls._get_serializable_fields().items():
            # print(">> Analysing '{}' => '{}'...".format(expected_field_name, expected_field_definition))
            
            # Checking if the field is present in the given data and fixing it if possible.
            if expected_field_name not in _temp_data_dict:
                # print(">> Not found in given dict !")
                # Checking if it has a default value in its class' definition.
                if expected_field_definition.default is MISSING:
                    raise ValueError("Could not get a default value for the '{}' expected field in '{}' !".format(
                        expected_field_name, cls.__name__
                    ))
                else:
                    # print(">> Assigned '{}' as default value !".format(expected_field_definition.default))
                    # TODO: Check if Field lists work properly !
                    _temp_data_dict[expected_field_name] = expected_field_definition.default
            
            # Getting some info on the field and its type for later.
            is_type_valid, field_simplified_type = cls._analyse_type(
                expected_type=expected_field_definition.type,
                actual_type=type(_temp_data_dict.get(expected_field_name)),
                process_listed_types=False)
            # print(">> Grabbed more info: is_type_Valid:{}, field_simplified_type:{}".format(
            #     is_type_valid, field_simplified_type
            # ))
            
            # Checking if the expected types are compatible.
            if validate_type and not is_type_valid:
                raise TypeError("The '{type_actual}' type is supported by '{type_expected}'".format(
                    type_actual=type(_temp_data_dict.get(expected_field_name)),
                    type_expected=expected_field_definition.type
                ))
            
            # print("FIELD_TYPE_UNKNOWN => '{}'".format(EFieldType.FIELD_TYPE_UNKNOWN))
            # print("FIELD_TYPE_PRIMITIVE => '{}'".format(EFieldType.FIELD_TYPE_PRIMITIVE))
            # print("FIELD_TYPE_ITERABLE => '{}'".format(EFieldType.FIELD_TYPE_ITERABLE))
            # print("FIELD_TYPE_SERIALIZABLE => '{}'".format(EFieldType.FIELD_TYPE_SERIALIZABLE))
            
            # Attempting to parse the data if, and only if, it is needed to do so.
            if field_simplified_type == EFieldType.FIELD_TYPE_ITERABLE:
                # We are checking for potentially listed 'ISerializable' classes.
                # print(">> Type: Is iterable !")
                
                is_listed_type_valid, listed_field_simplified_type = cls._analyse_type(
                    expected_type=get_args(expected_field_definition.type),
                    actual_type=type(_temp_data_dict.get(expected_field_name)[0]),
                    process_listed_types=True)
                # print(">> Grabbed more info on listed type: is_type_Valid:{}, field_simplified_type:{}".format(
                #     is_listed_type_valid, listed_field_simplified_type
                # ))
                
                """
                return [cls._deserialize_value(
                    value_class=get_args(value_class)[0],
                    value_data=x,
                    allow_unknown=allow_unknown
                ) for x in value_data]
                """
            
            if field_simplified_type == EFieldType.FIELD_TYPE_SERIALIZABLE:
                # print(">> Type: Is serializable ! -> {}".format(expected_field_definition.type))
                # print(">> |_> {}".format(_temp_data_dict.get(expected_field_name)))
                
                _temp_data_dict[expected_field_name] = expected_field_definition.type.from_dict(
                    data_dict=_temp_data_dict.get(expected_field_name),
                    allow_unknown=allow_unknown,
                    add_unknown_as_is=add_unknown_as_is,
                    allow_as_is_unknown_overloading=allow_as_is_unknown_overloading,
                    allow_missing_required=allow_missing_required,
                    allow_missing_nullable=allow_missing_nullable,
                    add_unserializable_as_dict=add_unserializable_as_dict,
                    validate_type=validate_type,
                    parsing_depth=parsing_depth - 1,
                    do_deep_copy=do_deep_copy,
                )
                
                # print(">> |_> {}".format(_temp_data_dict.get(expected_field_name)))
            else:
                # print(">> Type: Other/primitive/list, will be using it as-is !")
                pass
        
        # TODO: Implement check for nullable fields !
        # TODO: Unknowns & default values !
        
        if allow_unknown and add_unknown_as_is:
            # Preparing, modifying, and then returning the class.
            _tmp_class = cls(**_temp_data_dict)
            
            for unknown_field_name, unknown_field_value in _unknown_data.items():
                # print(">> Adding unknown field named '{}'".format(unknown_field_name))
                if hasattr(_tmp_class, unknown_field_name):
                    if allow_as_is_unknown_overloading:
                        # print(">> Will be overloading existing attribute !")
                        setattr(_tmp_class, unknown_field_name, unknown_field_value)
                    else:
                        # print(">> Cannot overload existing attribute, raising error !")
                        raise ValueError("The unknown field '{}' cannot overload existing attributes !".format(
                            unknown_field_name))
                else:
                    # print(">> Adding new non-existent attribute !")
                    setattr(_tmp_class, unknown_field_name, unknown_field_value)
            
            # Now returning the class :)
            return _tmp_class
        else:
            # Preparing and returning the class directly.
            return cls(**_temp_data_dict)
    
    @classmethod
    def from_json(cls, data_json: str, allow_unknown: bool = False, add_unknown_as_is: bool = False,
                  allow_as_is_unknown_overloading: bool = False, allow_missing_required: bool = False,
                  allow_missing_nullable: bool = True, add_unserializable_as_dict: bool = False,
                  validate_type: bool = True, parsing_depth: int = -1):
        """
        Deserialize a given json-encoded dict into the relevant serializable class.
        
        :param data_json: Json string containing the data to parse and then deserialize.
        :param allow_unknown: Allow unknown fields to be processed, other parameters will determine their use if 'True'.
        :param add_unknown_as_is: Adds unknown fields/values as-is in the final class if 'allow_unknown' is also 'True'.
        :param allow_as_is_unknown_overloading: Allow unknown fields/values to overload existing class attributes.
        :param allow_missing_required: ! Not used yet !
        :param allow_missing_nullable: ! Not used yet !
        :param add_unserializable_as_dict: ! Not used yet !
        :param validate_type: Enables a strict type check between the class' serializable fields and the given data.
        :param parsing_depth: The recursive depth to which the deserialization process will go.  (-1 means infinite)
        :return: The parsed 'ISerializable' class.
        :raises TypeError: If a mismatch between the expected and received data's types is found, requires
         'validate_type' to be set to 'True'.
        :raises ValueError: If an unknown field is given and cannot be allowed or added back in the final class.
        :raises JSONDecodeError: If the given 'data_json' is not a properly formatted JSON string.
        """
        
        return cls.from_dict(
            data_dict=json.loads(data_json),
            allow_unknown=allow_unknown,
            add_unknown_as_is=add_unknown_as_is,
            allow_as_is_unknown_overloading=allow_as_is_unknown_overloading,
            allow_missing_required=allow_missing_required,
            allow_missing_nullable=allow_missing_nullable,
            add_unserializable_as_dict=add_unserializable_as_dict,
            validate_type=validate_type,
            parsing_depth=parsing_depth,
            do_deep_copy=False,
        )


class IDeserializable(ABC):
    @classmethod
    def to_dict(cls):
        pass
    
    @classmethod
    def to_json(cls):
        return json.dumps(ISerializable.to_dict())
