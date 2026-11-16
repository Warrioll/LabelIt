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
    csvClasses=[]


    def clearProject():
         state.files.clear()
         state.currentImg=None
         state.selectedLabelBoxId =None

         state.classesList.clearLabelClassesList()
         
         state.imagesClassesList.clearImageClassesList()
         state.classesCounter=0
         ui.run_javascript('window.location.reload()')


    async def uploadHandler(e):
        nonlocal labelsData,  csvClasses
  
        for file in e.files:
            if file.content_type=='image/jpeg' or file.content_type=='image/png': 
                  #files.append( Image.open(io.BytesIO(await file.read())))
                  state.files.append( DatasetImage(await file.read(), file.name,file.content_type))
            elif file.content_type=='text/csv':
                pass
            elif file.content_type=='text/plain':
                fileData= await utils.readTXTFile(file)
                labelsData.append(fileData)
        usefullFiles=len(state.files)+len(csvClasses)+len(labelsData)#+len(jsonClasses)
        uslessFiles=len(e.files)-usefullFiles
        del e.files          
        ui.notify(f'{usefullFiles} file(s) uploaded!', classes='bg-white text-black') 
        if uslessFiles>0:
           ui.notify(f'{uslessFiles} files rejected becasue of bad extension',  classes='bg-red-700')
 
        state.classesList.classes.clear()
        notFoundImg =state.classesList.appendLabels(labelsData)
        if len(state.classesList.classes)==0: 
            state.classesList.classes.append(LabelClass(0,'my_class', state.labelColors[0]))
        if notFoundImg>0:
             ui.notify(f' Images not found for {notFoundImg} label files.',  classes='bg-white text-black')
        if len(state.files):
            ui.notify(f' Label files found for {len(labelsData)-notFoundImg} images.',  classes='bg-white text-black')
        
        if len(state.files)>0:
           goLabelButton.enable()

    
    with ui.row().classes(' my-color w-full min-h-screen justify-center p-0 m-0 flex'):

        with ui.column().classes('bg-linear-to-r min-h-screen from-yellow-500  to-amber-500 m-0 w-[40vw] h-full justify-center align-center items-end px-32'):
            # ui.html('''
            #     <div class='text-lg text-right text-black mb-8'>Upload <br/>images (JPG/PNG), <br/>labels (TXT) <br/> and annotations (JSON) here: </div>
            # ''')
            ui.label('Upload files here:').classes('text-xl text-right text-black mb-8')
            upload = ui.upload(on_multi_upload=uploadHandler,  
                      on_rejected=lambda: ui.notify('Rejected!',classes='bg-red-700'),  multiple=True).classes('bg-red-500')\
                      .classes('w-full bg-stone-900 h-[34rem] max-h-[100vh] rounded-lg')
            ui.button('Clear added, not uploaded files ', on_click=upload.reset).classes('w-full rounded-lg mt-8 ').props('outline color=black')
            goLabelButton = ui.button('Label/Annotate images ', icon='arrow_forward_outline', on_click=lambda: ui.navigate.to('/workspace')).classes('w-full rounded-lg mt-3 bg-white text-black') 
            goLabelButton.disable()

        with ui.column().classes('p-0 pl-64 bg-linear-to-r min-h-screen from-stone-800 to-stone-900 w-[60vw] m-0 justify-center  items-start'):
            ui.html(''' <div class="w-[80%] text-white text-[4rem]  h-full">
            Welcome to 
            <strong class="text-[9rem] mb-0">
                <span class="text-yellow-500  mb-0">Label</span>It<span class="text-yellow-500  mb-0">!</span>
            </strong>
             <br/><div class="text-2xl subtitle -mt-4">Upload your dataset and label or annotate <span class="text-yellow-500">it</sapn><span class="text-white">!</sapn></div>
            </div>''', sanitize=False)