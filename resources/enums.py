import enum

class TextType(enum.Enum):
    TEXT = 0
    KEYWORD = 1
    REF = 2
    IMG = 3
    
class RenderType(enum.Enum):
    IMG = 0
    TEXT = 1
