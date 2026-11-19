from typeguard import typechecked
from classes.ImageClass import ImageClass
import state
import utils

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

    def clearImageClassesList(self):
         self.classes.clear()
         self.classes=[ImageClass('my_class')]
    def appendClass(self, className:str)-> ImageClass|None:
         if self.checkIfClassNameAvailable(className, None):
              newClass= ImageClass(className)
              self.classes.append(newClass)
              return newClass
         else:
              return None

    def appendAnnotations(self, classes:list[str], annotations:list[dict]) ->list[str]:
        foundNames=[]
        for cls in classes:
              self.appendClass(cls)
        for annotation in annotations:
            imgName=utils.getFileNameWithoutExtension(annotation['name'])
            img=None
            for im in state.files:
                  if imgName==utils.getFileNameWithoutExtension(im.name):
                        img=im
                        break
            if img is None:
                #notFount.append(annotation['name'])
                continue
            foundNames.append(img.name)
            for imCls in classes:
                 if annotation[imCls]:
                      clsObj=next((cls for cls in self.classes if cls.className == imCls), None)
                      if clsObj is not None:
                           img.appendClass(clsObj)
        return foundNames

    # def appendMultipleClasses(self, classesNames: list[str]):
    #      for name in classesNames:
              