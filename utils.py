from nicegui import ui
from classes.DatasetImage import DatasetImage
import io
import zipfile
from datetime import datetime
import json
import csv
from nicegui.elements.upload_files import SmallFileUpload
from classes.ImageClass import ImageClass

def basicAppSettings(pageSubtitle: str=''):
        ui.page_title('LabelIt! - '+pageSubtitle)
        ui.add_head_html('''
<style>
:root{
--nicegui-default-padding: 0rem;
--nicegui-default-gap: 0rem;

color: white;
background-color: oklch(21.6% 0.006 56.043);
}

</style>
''')


def getCurrentDateStringForFileName()->str:
      return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

def createObjectDecectionZip(files: list[DatasetImage]):
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in files:
                name=file.name.split('.')
                name.pop()
                zip_file.writestr(f'{'.'.join(name)}.txt', '\n'.join(file.getBoxesDataForYOLO()))
           

        zip_buffer.seek(0)
        return zip_buffer.getvalue()

def createImageRecognitionJSONFile(files: list[DatasetImage]):
        data=[]
        for i in range(len(files)):
              data.append(files[i].getImageRecognitionDataForJSON())
        content =json.dumps(data, indent=4, ensure_ascii=False).encode('utf-8')
        return  content

# def createImageRecognitionCSVFile(files: list[DatasetImage]):
#         data=[]
#         #buffer = io.StringIO()
#         #writer = csv.writer(buffer, quoting=csv.QUOTE_NONE, escapechar='\\')

#         for file in files:
#               data.append(','.join(file.getImageRecognitionDataForCSV()))
#         #       name, annotations = file.getImageRecognitionDataForCSV()
#         #       writer.writerow([
#         #          name,
#         #         f'"{annotations}"'
#         #])

#         return '\n'.join(data).encode('utf-8-sig')

def createImageRecognitionCSVFile(files: list[DatasetImage], classesList:list[ImageClass]):
    buffer = io.StringIO(newline='')
    writer = csv.writer(buffer, delimiter=';')

    header = ['index', 'nazwa_pliku_img']
    for imgCls in classesList:
        header.append(imgCls.className)

    writer.writerow(header)

    for i, file in enumerate(files):
        row = file.getImageRecognitionDataForCSV(classesList)

        # Dodanie indeksu do początku wiersza
        row.insert(0, i)

        writer.writerow(row)

    return buffer.getvalue().encode('utf-8-sig')

async def readTXTFile(file:SmallFileUpload) -> dict|None:
        
        contentAll = (await file.read()).decode('utf-8')
        lines=contentAll.split('\n')
        data=[]
        fileData={'name': file.name}

        if not contentAll.strip():
                fileData['boxes'] = data
                return fileData

        for line in lines:
               sep=line.split(' ')
               if len(sep)!=5:
                      return None
               try:
                      classId=int(sep[0])
                      centerX=float(sep[1])
                      centerY=float(sep[2])
                      width=float(sep[3])
                      height=float(sep[4])
               except  Exception:
                      return None
               
               data.append([classId, centerX,centerY,width,height])
        fileData['boxes']=data
        return fileData

def findCurrentImgIndex(files:list[DatasetImage], objToFind:DatasetImage)->int:
       return files.index(objToFind)


def getFileNameWithoutExtension(fileName:str):
      name=fileName.split('.')
      name.pop()
      return '.'.join(name)
    

async def readCSVFile(file:SmallFileUpload) -> tuple[list[str], list[dict]]:
                reader = csv.reader(io.StringIO((await file.read()).decode("utf-8")), delimiter=";")
                rows = list(reader)
                classes=list(rows)[0][2:].copy()
                imgToClasses=[]
                
                for i, wiersz in enumerate(rows):
                        if i==0:
                               continue
                        else:
                                tmp={"name": wiersz[1]}
                                for j in range(2,len(wiersz)):
                                       tmp[classes[j-2]]=wiersz[j]=='1'
                                imgToClasses.append(tmp)
                return classes, imgToClasses

