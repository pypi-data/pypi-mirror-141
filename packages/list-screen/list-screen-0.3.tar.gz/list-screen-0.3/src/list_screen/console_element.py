from typing import Union
from .dynamic_element import DynamicElement

console_element = Union[str, DynamicElement]
line_type = Union[str, list[console_element]]
