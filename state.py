from classes.DatasetImage import DatasetImage
from pathlib import Path
from classes.LabelClassesList import LabelClassesList
from classes.ImageClass import ImageClass
from classes.ImageClassesList import ImageClassesList 
from typing import Callable
from nicegui import ui

labelColors=[
    {'name': 'white', "value": '#ffffff'},
    {'name': 'black', "value": '#000000'},
    {'name': 'tomato', "value": '#f06418'},
    {'name': 'yellow', "value": '#d9d02f'},
    {'name': 'green', "value": '#2bdd66'},
    {'name': 'sky blue', "value": '#099cff'},
    {'name': 'violet', "value": '#c02adf'},
    {'name': 'magenta', "value": '#f01879'},
    {'name': 'gray', "value": '#777c91'},
    {'name': 'orange', "value": '#fc8a08'},
    {'name': 'brown', "value": '#5d4037'},
    {'name': 'seagreen', "value": '#00ffb3'},
    {'name': 'red', "value": '#f21616'},
    {'name': 'dark violet', "value": '#6b31b2'},
    {'name': 'deep blue', "value": '#2c40dc'},
    {'name': 'light blue', "value": '#99e2ff'},
    {'name': 'pink', "value": '#faa1f6'},
    {'name': 'bright orange', "value": '#ffa903'},
    {'name': 'neon lime', "value": '#c8ff03'},
    {'name': 'light gray', "value": '#c8cad3'}, 
    {'name': 'dark green', "value": '#4da91b'},
    {'name': 'pale red', "value": '#b41148'},
    #{'name': 'pale blue', "value": '#504c97'},
    {'name': 'dark gray', "value": '#4a5167'},
    {'name': 'pale orange', "value": '#ffb45e'},
    {'name': 'dark blue', "value": '#0a259c'},
]

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

classesList:LabelClassesList = LabelClassesList()
imagesClassesList:ImageClassesList =ImageClassesList ()
classesCounter=0




    #selectedImgButton:ui.button|None=None
def setImgAsCurrentImg(img: DatasetImage, canvasHandler: Callable):
            global currentImg
            btnMarkup='bg-amber-400 text-stone-900'
            labelMarkup='text-stone-900'
            
            currentImg.button.classes(remove=btnMarkup)
            currentImg.buttonLabel.classes(remove=labelMarkup)
            
            #nonlocal selectedImgButton
            currentImg=img

            currentImg.button.classes(add=btnMarkup)
            currentImg.buttonLabel.classes(add=labelMarkup)

            refreshFooter()

            canvasHandler()

            # canvas.eraseAllBoxes()
            # canvas.setNewCanvasImgAndScale(imgW, imgH)

            # canvas.drawAllCurrrentImgBoxes()





            # if not (selectedImgButton is None):
            #     selectedImgButton.classes(remove=markup)
            #     elements = selectedImgButton.descendants()
            #     label = next((el for el in elements  if isinstance(el, ui.label)), None)
            #     label.classes(remove='text-stone-900')
            #     label.classes(add='text-amber-400')
            # selectedImgButton=e.sender
            # selectedImgButton.classes(markup)
            # elements = selectedImgButton.descendants()
            # label = next((el for el in elements  if isinstance(el, ui.label)), None)
            # label.classes(add='text-stone-900')
            refreshBoxesList()
            refreshClassesList()

def clearProject():
    files.clear()
    currentImg=None
    selectedLabelBoxId =None
    classesList.clearLabelClassesList()         
    imagesClassesList.clearImageClassesList()
    classesCounter=0
    ui.run_javascript('window.location.reload()')