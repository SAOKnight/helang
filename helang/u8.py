from typing import *


class U8:
    """
    The Saint He's specific type.
    """
    def __init__(self, value: Optional[List[int]] = None):
        self.value = value

    def __str__(self) -> str:
        if self.value is None:
            return ''
        return ' | '.join(str(element) for element in self.value)
