from typeguard import typechecked
import state
from LabelClass import LabelClass
from Box import Box
import utils
 

@typechecked
class LabelClassesList:
    classes: list[LabelClass]
    nonClass:LabelClass

    def __init__(self):
        self.classes=[LabelClass(0,'my_class', state.labelColors[0])]
        self.nonClass=LabelClass(None, None, state.labelColors[0])

    def getExampleClass(self) -> LabelClass:
        return self.classes[0]

    def getClassesNames(self):
        return [ c.className for c in self.classes]

    def getClassesNamesNonClass(self):
            return [ c.className for c in self.classes].insert(0, self.nonClass.className)

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
    def addNewClass(self):
        tmpId=0
        while(not self.checkIfClassIdAvailable(tmpId, None)):
            tmpId+=1

        tmpClass=1
        className='new_class_'
        while(not self.checkIfClassNameAvailable(className+str(tmpClass), None)):
                    tmpClass+=1
        self.classes.append(LabelClass(tmpId,className+str(tmpClass), state.labelColors[0]))

    def uploadClass(self, classId:int, ) -> LabelClass:
        if self.checkIfClassIdAvailable(classId, None):
            tmpClass=1
            className='class_'
            while(not self.checkIfClassNameAvailable(className+str(tmpClass), None)):
                                 tmpClass+=1
            labelClass=LabelClass(classId,className+str(tmpClass))
            self.classes.append(labelClass)
            return labelClass
        else:
              return  None
         

    def appendLabels(self, data:list[dict]) -> int:
         notFountCounter=0

         for imgData in data:
              print(imgData['name'])
              imgName=utils.getFileNameWithoutExtension(imgData['name'])
              img=None
              for im in state.files:
                    if imgName==utils.getFileNameWithoutExtension(im.name):
                          img=im
                          break
              #img = next((im for im in state.files if im.name == imgData['name']), None)
              if img is None:
                   notFountCounter+=1
                   continue
              for b in imgData["boxes"]:
                   classId=b[0]
                   labelClass = next((cls for cls in self.classes if cls.classId == classId), None)
                   if labelClass is None:     
                        labelClass=self.uploadClass(classId)
                   w, h = img.getImageSize()
                   img.appendBox(Box(state.boxCounter, (b[1]*w- b[3]*w/2, b[2]*h-b[4]*h/2), b[3]*w, b[4]*h, labelClass))
                   state.boxCounter+=1
         return notFountCounter