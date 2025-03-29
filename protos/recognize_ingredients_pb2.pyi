from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RecognizeIngredientsStreamRequest(_message.Message):
    __slots__ = ("image",)
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    image: bytes
    def __init__(self, image: _Optional[bytes] = ...) -> None: ...

class RecognizeIngredientsResponse(_message.Message):
    __slots__ = ("ingredients",)
    INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
    ingredients: _containers.RepeatedCompositeFieldContainer[RecognizeIngredientsIngredient]
    def __init__(self, ingredients: _Optional[_Iterable[_Union[RecognizeIngredientsIngredient, _Mapping]]] = ...) -> None: ...

class RecognizeIngredientsIngredient(_message.Message):
    __slots__ = ("name", "x", "y", "width", "height")
    NAME_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    name: str
    x: float
    y: float
    width: float
    height: float
    def __init__(self, name: _Optional[str] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., width: _Optional[float] = ..., height: _Optional[float] = ...) -> None: ...
