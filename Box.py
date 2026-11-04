from typeguard import typechecked
from LabelClass import LabelClass

@typechecked
class Box:
    boxId:int
    position:tuple[float, float]
    width:float
    height:float
    labelClass: LabelClass

    def __init__(self, boxId:int, topLeft:tuple[float, float],  width:float,height:float, labelClass:LabelClass|None =None):
        self.boxId=boxId
        self.position=topLeft
        self.width=width
        self.height=height
        self.labelClass=labelClass

    def changeClassName(self, labelClass: LabelClass):
        print
        self.labelClass=labelClass