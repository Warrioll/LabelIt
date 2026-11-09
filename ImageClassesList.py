from typeguard import typechecked
import state
from ImageClass import ImageClass

@typechecked
class ImageClassesList:
    classes: list[ImageClass]
    nonClass:ImageClass

    def __init__(self):
        self.classes=[ImageClass('my_class')]
        self.nonClass=ImageClass( None)

    def getExampleClass(self) -> ImageClass:
        return self.classes[0]

    def getClassesNames(self):
        return [ c.className for c in self.classes]

    def getClassesNamesNonClass(self):
            return [ c.className for c in self.classes].insert(0, self.nonClass.className)

    def getClassByName(self, name:str):
        return  next((obj for obj in self.classes if obj.className == name), None)


    def checkIfClassNameAvailable(self, nameToCheck: str, excludeClass) -> bool:
        return not any(
            c.className == nameToCheck and c is not excludeClass
            for c in self.classes
        )
    def addNewClass(self):
        tmpClass=1
        className='new_class_'
        while(not self.checkIfClassNameAvailable(className+str(tmpClass), None)):
                    tmpClass+=1
        self.classes.append(ImageClass(className+str(tmpClass)))
