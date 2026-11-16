from typeguard import typechecked
import uuid 


@typechecked
class LabelClass:
    innerId:str
    className:str|None
    classId:int|None
    color: dict[str, str]|None

    def __init__(self, classId: int|None, className:str|None, color: dict[str, str]):
        self.classId=classId
        self.className=className
        self.innerId=self.innerId = uuid.uuid4().hex
        self.color=color      

    def setClassName(self, className:str):
        self.className=className
    def setClassId(self, classId:int):
        self. classId= classId