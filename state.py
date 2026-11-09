from DatasetImage import DatasetImage
from pathlib import Path
from LabelClassesList import LabelClassesList
from ImageClass import ImageClass
from ImageClassesList import ImageClassesList 

currentImg: DatasetImage| None = None
files:list[DatasetImage]=[
            # DatasetImage(Path('/home/karol/datasets/PV-farm1/images/DJI_20240709121026_0097_T.JPG'),'DJI_20240709121026_0097_T.JPG'),
            # DatasetImage(Path('/home/karol/datasets/PV-farm1/images/DJI_20240709120928_0015_T.JPG'),'DJI_20240709120928_0015_T.JPG'),
            # DatasetImage(Path('/home/karol/datasets/PV-farm1/images/DJI_20240709120938_0029_T.JPG'),'DJI_20240709120938_0029_T.JPG'),
            # DatasetImage(Path('/home/karol/datasets/PV-farm1/images/DJI_20240709121044_0123_T.JPG'),'DJI_20240709121044_0123_T.JPG'),
            # DatasetImage(Path('/home/karol/datasets/PV-farm1/images/DJI_20240709122552_0143_T.JPG'),'DJI_20240709122552_0143_T.JPG'),

            # DatasetImage(Path('C:\\Users\\lorak\\Desktop\\magisterka\\datasets\\Farma 2\\DJI_20230921113850_0001_T.JPG'),'DJI_20230921113850_0001_T.JPG'),
            # DatasetImage(Path('C:\\Users\\lorak\\Desktop\\magisterka\\datasets\\Farma 2\\DJI_20230921113854_0006_T.JPG'),'DJI_20230921113854_0006_T.JPG'),
            # DatasetImage(Path('C:\\Users\\lorak\\Desktop\\magisterka\\datasets\\Farma 2\\DJI_20230921113935_0063_T.JPG'),'DJI_20230921113935_0063_T.JPG'),
]
refreshBoxesList=None
refreshClassesList=None
refreshFooter=None
selectedLabelBoxId:int|None =None

boxCounter=0

classesList:LabelClassesList = LabelClassesList()
imagesClassesList:ImageClassesList =ImageClassesList ()
classesCounter=0