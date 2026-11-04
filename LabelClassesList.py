from typeguard import typechecked
import state
from LabelClass import LabelClass

@typechecked
class LabelClassesList:
    classes: list[LabelClass]

    def __init__(self):
        self.classes=[LabelClass(0,'my_class'), LabelClass(1,'my_class2')]

    def getExampleClass(self) -> LabelClass:
        return self.classes[0]

    def getClassesNames(self):
        return [ c.className for c in self.classes]

    def getClassByName(self, name:str):
        return  next((obj for obj in self.classes if obj.className == name), None)

    def checkIfClassIdAvailable(self, idToCheck: int, excludeClass) -> bool:
        return not any(
            c.classId == idToCheck and c is not excludeClass
            for c in self.classes
        )

    def checkIfClassNameAvailable(self, nameToCheck: str, excludeClass) -> bool:
        return not any(
            c.className == nameToCheck and c is not excludeClass
            for c in self.classes
        )