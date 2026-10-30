from nicegui import ui
from utils import basicAppSettings
from PIL import Image
import io

def homePage(files: list):
    basicAppSettings('Home')
    ui.add_css("""
                .q-uploader__header {
                background-color: transparent;
                  }
                """)



    async def uploadHandler(e):
  
         for file in e.files:
            if file.content_type=='image/jpeg' or file.content_type=='image/png': 
                   files.append( Image.open(io.BytesIO(await file.read())))
         uploadedLen=len(e.files)
         del e.files          
         ui.notify(f'{len(files)} files uploaded!', classes='bg-white text-black')
         if uploadedLen-len(files)>0:
            ui.notify(f'{uploadedLen-len(files)} files rejected becasue of bad extension',  classes='bg-red-700')

         if len(files)>0:
            goLabelButton.enable()
         
         

    
    with ui.row().classes(' my-color w-full min-h-screen justify-center p-0 m-0 flex'):

        with ui.column().classes('bg-linear-to-r min-h-screen from-yellow-500  to-amber-500 m-0 w-[40vw] h-full justify-center align-center items-end px-32'):
            ui.html('''
                <div class='text-xl text-black mb-8'>Upload your images here: </div>
            ''')
            ui.upload(on_multi_upload=uploadHandler,  
                      on_rejected=lambda: ui.notify('Rejected!',classes='bg-red-700'),  multiple=True).classes('bg-red-500')\
                      .classes('w-full bg-stone-900 h-[34rem] max-h-[100vh] rounded-lg')
            goLabelButton = ui.button('Label images ', icon='arrow_forward_outline', on_click=lambda: ui.navigate.to('/workspace')).classes('w-full rounded-lg mt-8 bg-white text-black') 
            goLabelButton.disable()

        with ui.column().classes('p-0 pl-64 bg-linear-to-r min-h-screen from-stone-800 to-stone-900 w-[60vw] m-0 justify-center  items-start'):
            ui.html(''' <div class="w-[80%] text-white text-[4rem]  h-full">
            Welcome to 
            <strong class="text-[9rem] mb-0">
                <span class="text-yellow-500  mb-0">Label</span>It<span class="text-yellow-500  mb-0">!</span>
            </strong>
             <br/><div class="text-2xl subtitle -mt-4">Upload images and label your dataset.</div>
            </div>''', sanitize=False)