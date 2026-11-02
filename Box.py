from typeguard import typechecked

@typechecked
class Box:
    boxId:int
    position:tuple[float, float]
    width:float
    height:float
    className:str |None

    def __init__(self, boxId:int, topLeft:tuple[float, float],  width:float,height:float, className:str|None =None):
        self.boxId=boxId
        self.position=topLeft
        self.width=width
        self.height=height
        self.className=className

    def changeClassName(self, className:str):
        self.className=className