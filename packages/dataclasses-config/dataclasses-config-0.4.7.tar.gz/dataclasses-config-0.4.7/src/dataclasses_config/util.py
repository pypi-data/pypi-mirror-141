from dataclasses import fields, Field, dataclass
from functools import partial, wraps
from typing import *

from dataclasses_json import Undefined, DataClassJsonMixin
from pyhocon import ConfigTree, HOCONConverter

def get_field(class_or_instance, field_name: str) -> Field:
    """
    Extracts the `dataclasses.Field` object from the class or instance metadata.
    
    Args:
        class_or_instance: a DataClass class or instance (`dataclasses.is_dataclass()` should return `True`)
        field_name: `str`. A field name to find.
    
    Returns:
        `dataclasses.Field`
    
    """
    
    try:
        _cls_f: Field = next(f for f in fields(class_or_instance) if f.name == field_name)
    except StopIteration as e:
        raise AttributeError(f"Dataclass {class_or_instance!r} does not have the attribute {field_name!r}.") from e
    else:
        return _cls_f

def dump_config(conf: ConfigTree, format: str = 'json', prefix: str = "Config dump:") -> str:
    """
    Dumps the specified `pyhocon.ConfigTree` in specified format.
    
    Args:
        conf: `pyhocon.ConfigTree` to dump.
        format: `str`.
            For the *pyhocon* release 0.4.0, the following formats are allowed:
            
             - `json` *(default)*
             - `properties`
             - `hocon`
             - `yaml`
        
        prefix: `str`. A string which would be printed before the config.
    
    Returns:
        `str`. A string representation of config in specified format.
    
    """
    lines = \
    [
        prefix,
        # '[START]',
        HOCONConverter.convert(conf, format),
        # '[END]',
    ]
    
    return '\n'.join(lines)

CLASS_WRAPS_UPDATES = \
[
    '__annotations__',
]
_wraps_class = wraps(wraps)(partial(wraps, updated=CLASS_WRAPS_UPDATES))
_wraps_class.__doc__ += \
"""
    This function is compatible with the classes, abstract classes and dataclasses wrapping
    in the newer Python versions.
    This function does not update `__dict__` by default, but updates `__annotations__` instead,
    which is required for the popper dataclasses work.
"""

@wraps(_wraps_class)
def wraps_class(*args, **kwargs):
    return _wraps_class(*args, **kwargs)

T = TypeVar('T')
@dataclass(frozen=True)
class DataclassesJsonMeta(DataClassJsonMixin):
    """
    A helper class representing a content of `dataclasses_json.config()` metadata structure.
    
    See Also:
        * `dataclasses.Field.metadata`
        * `dataclasses_json.cfg.config()`
    """
    
    encoder: Optional[Callable] = None
    decoder: Optional[Callable] = None
    mm_field: Any = None
    letter_case: Optional[Callable[[str], str]] = None
    undefined: Optional[Union[str, Undefined]] = None
    exclude: Optional[Callable[[str, T], bool]] = None


__all__ = \
[
    'dump_config',
    'get_field',
    'wraps_class',
    
    'CLASS_WRAPS_UPDATES',
    
    'DataclassesJsonMeta',
]
