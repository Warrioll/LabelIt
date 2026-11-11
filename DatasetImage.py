from typeguard import typechecked
import base64
from PIL import Image
from pathlib import Path
from io import BytesIO
from Box import Box
from ImageClass import ImageClass

@typechecked
class DatasetImage:
    imgBytes:bytes
    name: str
    mime:str
    boxes: list[Box]
    imageClasses: list[ImageClass]
    status:SyntaxWarning
    refreshBadge=None

    def __init__(self, img:bytes| Path, name:str, mime:str | None=None):
        if isinstance(img, bytes):
            self.imgBytes=img
        else:
            self.imgBytes=img.read_bytes()
        self.name=name
        if mime is None:
            self.mime=self.getMimeType()
        else:
            self.mime=mime
        self.boxes=[]
        self.imageClasses=[]
        self.status='Todo'
        self.refreshBadge=None

    def getUrl(self) -> str:
        return f'data:{self.mime};base64,{base64.b64encode(self.imgBytes).decode()}'
    
    def getPIL(self)-> Image:
        return Image.open(BytesIO(self.imgBytes))

    def getMimeType(self) -> str:
        with Image.open(BytesIO(self.imgBytes)) as img:
            return Image.MIME[img.format]

    def getImageSize(self) -> tuple[int, int]:
        with Image.open(BytesIO(self.imgBytes)) as img:
                    return img.width, img.height

    def appendBox(self,box:Box):
         self.boxes.append(box)

    def appendClass(self, imageClass: ImageClass):
         self.imageClasses.append(imageClass)
    def removeClass(self, imageClass: ImageClass):
         self.imageClasses.remove(imageClass)

    def getBoxesDataForYOLO(self) ->list[str]:
        w, h = self.getImageSize()
        lines=[]
        for box in self.boxes:
              data=box.getBoxDataForYOLO()
              lines.append(f'{str(data[0])} {str(data[1]/w)} {str(data[2]/h)} {str(data[3]/w)} {str(data[4]/h)}')
        return lines

    def getImageRecognitionDataForJSON(self)->dict:
        annotations=[]
        for i in range(len(self.imageClasses)):
              annotations.append(self.imageClasses[i].className)
        return {
             "image": self.name,
             "annotations": annotations
                }
    # def getImageRecognitionDataForCSV(self)->list[str, str]:
    #      classes=[cls.className for cls in self.imageClasses]
    #      return [self.name, '"['+','.join(classes)+']"']

    def getImageRecognitionDataForCSV(self, classesList: list[ImageClass])->list:
         row=[self.name]
         for cls in classesList:
            isAssigned=False
            for imgCls in self.imageClasses:
                   if imgCls.innerId==cls.innerId:
                        isAssigned=True
                        break
            if isAssigned:
                 row.append(1)
            else:
                 row.append(0)
            
         return row
    
    def updateStatus(self,newStatus:str):
         if newStatus=='Todo' or newStatus=='Done' or newStatus=='Review':
              self.status=newStatus
              self.refreshBadge()