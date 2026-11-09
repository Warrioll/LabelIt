from typeguard import typechecked
from uuid import uuid4

@typechecked
class LabelClass:
    innerId:str
    className:str|None
    classId:int|None

    def __init__(self, classId: int|None, className:str|None):
        self.classId=classId
        self.className=className
        self.innerId=self.innerId = str(uuid4())
       

    def setClassName(self, className:str):
        self.className=className
    def setClassId(self, classId:int):
        self. classId= classId