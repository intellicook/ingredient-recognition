from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SelectIngredientStreamRequest(_message.Message):
    __slots__ = ("image", "x", "y")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    image: bytes
    x: int
    y: int
    def __init__(self, image: _Optional[bytes] = ..., x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class SelectIngredientStreamResponse(_message.Message):
    __slots__ = ("image", "name")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    image: bytes
    name: str
    def __init__(self, image: _Optional[bytes] = ..., name: _Optional[str] = ...) -> None: ...
