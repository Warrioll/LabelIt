from typeguard import typechecked
import base64
from PIL import Image
from pathlib import Path
from io import BytesIO
from Box import Box

@typechecked
class DatasetImage:
    imgBytes:bytes
    name: str
    mime:str
    boxes: list[Box]

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