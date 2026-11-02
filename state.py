from DatasetImage import DatasetImage
from pathlib import Path

currentImg: DatasetImage| None = None
files:list[DatasetImage]=[
    DatasetImage(Path('/home/karol/datasets/PV-farm1/images/DJI_20240709121026_0097_T.JPG'),'tmpImg1'),
            DatasetImage(Path('/home/karol/datasets/PV-farm1/images/DJI_20240709120928_0015_T.JPG'),'tmpImg2'),
            DatasetImage(Path('/home/karol/datasets/PV-farm1/images/DJI_20240709120938_0029_T.JPG'),'tmpImg3'),
            DatasetImage(Path('/home/karol/datasets/PV-farm1/images/DJI_20240709121044_0123_T.JPG'),'tmpImg4'),
            DatasetImage(Path('/home/karol/datasets/PV-farm1/images/DJI_20240709122552_0143_T.JPG'),'tmpImg5'),
]
refreshBoxesList=None
classesList:dict[str, int]={'my_class':0, "pv_panel": 1}