from typeguard import typechecked
import uuid

@typechecked
class ImageClass:
    innerId:str
    className:str|None

    def __init__(self, className:str|None):
        self.className=className
        self.innerId= uuid.uuid4().hex
       

    def setClassName(self, className:str):
        self.className=className