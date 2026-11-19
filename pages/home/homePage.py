from nicegui import ui
import  utils
from PIL import Image
import io
from classes.DatasetImage import DatasetImage
from classes.LabelClass import LabelClass
import state

def homePage():
    utils.basicAppSettings('Home')
    ui.add_css("""
                .q-uploader__header {
                background-color: transparent;
                  }
                """)

    labelsData=[]
    csvFiles=[]

    async def uploadHandler(e):
        nonlocal labelsData,  csvFiles


        uslessFiles=[]
        for file in e.files:
            if file.content_type=='image/jpeg' or file.content_type=='image/png': 
 
                  state.files.append( DatasetImage(await file.read(), file.name,file.content_type))
            elif file.content_type=='text/csv':
                csvFiles.append(file)
            elif file.content_type=='text/plain':
                print(file.name)
                fileData= await utils.readTXTFile(file)
                labelsData.append(fileData)
            else:
                print('useless!')
                uslessFiles.append(file)
        usefullFiles=len(state.files)+len(csvFiles)+len(labelsData)#+len(jsonClasses)
        uslessFilesAmount=len(uslessFiles)
        for uf in uslessFiles:
            e.sender.remove_upload(uf)
        del e.files    
        if uslessFilesAmount>0:
           ui.notify(f'{uslessFilesAmount} files rejected becasue of bad extension',  classes='bg-red-700')
 
        state.classesList.classes.clear()
        foundLabelsPerImg =state.classesList.appendLabels(labelsData)
        if len(state.classesList.classes)==0: 
            state.classesList.classes.append(LabelClass(0,'my_class', state.labelColors[0]))

        csvFoundImgsCounter=[]
        annotationfPerImg=[]
        for csvFile in csvFiles:
            clss, annot = await utils.readCSVFile(csvFile)
            annotationfPerImg.extend([x["name"] for x in annot])
            csvFoundImgsCounter.extend(state.imagesClassesList.appendAnnotations(clss, annot))

        if not (len(state.files)==0 and len(csvFiles)==0 and len(labelsData)==0):
            notifyStr=''
            labelsPerImg=[x["name"] for x in labelsData]
            notifyStr+=f'<strong>Files uploaded: {len(state.files)}</strong> images, <strong>{len(labelsData)}</strong> TXT files, <strong>{len(csvFiles)}</strong> CSV files</strong>\n\n'
            notifyStr+=f'• Found  labels for <strong>{len(set(labelsPerImg))}</strong> images, <strong>{len(set(foundLabelsPerImg))}</strong> matching with uploaded images\n'
            notifyStr+=f'• Found  annotations for <strong>{len(set(annotationfPerImg))}</strong> images, <strong>{len(set(csvFoundImgsCounter))}</strong> matching with uploaded images\n'

            ui.html('<style>.multi-line-notification { white-space: pre-line; }</style>', sanitize=False)
            ui.notification(notifyStr, multi_line=True,classes='bg-white text-black multi-line-notification', html=True, timeout=15.0)



        
        if len(state.files)>0:
           goLabelButton.enable()


    def clearHandler():
        upload.reset()
        state.clearProject()

    
    with ui.row().classes(' my-color w-full min-h-screen justify-center p-0 m-0 flex'):

        with ui.column().classes('p-0 pl-[6vw] bg-linear-to-r min-h-screen from-stone-800 to-stone-900 w-[40vw] m-0 justify-center  items-start'):
                   ui.html(''' <div class="w-[80%] text-white text-[64px]  h-full">
                   Welcome to 
                   <strong class="text-[144px] mb-0">
                       <span class="text-yellow-500  mb-0">Label</Labelspan>It<span class="text-yellow-500  mb-0">!</span>
                   </strong>
                    <br/><div class="text-[24px] subtitle -mt-4">Upload your dataset and label or annotate <span class="text-yellow-500">it</sapn><span class="text-white">!</sapn></div>
                   </div>''', sanitize=False)
        with ui.column().classes('bg-linear-to-r min-h-screen from-yellow-500  to-amber-500 m-0 w-[60vw] h-full justify-center align-center items-start px-32'):
          
            ui.label('Upload files here:').classes('text-[20px]  text-left text-black mb-8')
            upload = ui.upload(on_multi_upload=uploadHandler,  
                      on_rejected=lambda: ui.notify('Rejected!',classes='bg-red-700'),  multiple=True).classes('bg-red-500')\
                      .classes('w-full bg-stone-900 h-[544px] max-h-[100vh] rounded-lg').props('accept=".jpg,.jpeg,.png,.txt,.csv"')
            ui.button('Upload files ', on_click=lambda: upload.run_method('upload')).classes('w-full rounded-lg mt-5 items-center text-white bg-stone-800').props('color=stone')
            ui.button('Remove all uploaded files ',on_click=clearHandler).classes('w-full rounded-lg mt-3 items-center').props(' outline color=black')
            goLabelButton = ui.button('Label/Annotate images ', on_click=lambda: ui.navigate.to('/workspace')).classes('w-full rounded-lg mt-3 mb-8 bg-white text-black')
            goLabelButton.disable()

       