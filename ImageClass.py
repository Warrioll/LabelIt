from typeguard import typechecked
from uuid import uuid4

@typechecked
class ImageClass:
    innerId:str
    className:str|None

    def __init__(self, className:str|None):
        self.className=className
        self.innerId=str(uuid4())
       

    def setClassName(self, className:str):
        self.className=className