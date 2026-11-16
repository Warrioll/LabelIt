from typeguard import typechecked
from classes.LabelClass import LabelClass
import uuid


@typechecked
class Box:
    boxId:str
    position:tuple[float, float]
    width:float
    height:float
    labelClass: LabelClass

    def __init__(self,topLeft:tuple[float, float],  width:float,height:float, labelClass:LabelClass|None =None):
        self.boxId= uuid.uuid4().hex#boxId
        self.position=topLeft
        self.width=width
        self.height=height
        self.labelClass=labelClass

    def changeClassName(self, labelClass: LabelClass):
        self.labelClass=labelClass

    def getBoxDataForYOLO(self) -> tuple[int, float, float, float, float]:
        centerX=self.position[0]+self.width/2
        centerY=self.position[1]+self.height/2
        return self.labelClass.classId, centerX, centerY, self.width, self.height

    def getBoxCopy(self) ->Box:
        return Box((self.position[0],self.position[1]), self.width, self.height, self.labelClass)