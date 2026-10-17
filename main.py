from nicegui import ui

APP_URL='http://127.0.0.1:8080/'

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


goodFiles=[]

@ui.page('/')
def workspacePage():
    basicAppSettings('Home')
    ui.add_css("""
                .q-uploader__header {
                background-color: transparent;
                  }
                """)



    def uploadHandler(e):
  
         for file in e.files:
              print(file.content_type)
              if file.content_type=='image/jpeg' or file.content_type=='image/png': 
                   goodFiles.append(file)
         uploadedLen=len(e.files)
         del e.files          
         ui.notify(f'{len(goodFiles)} files uploaded!', classes='bg-white text-black')
         if uploadedLen-len(goodFiles)>0:
            ui.notify(f'{uploadedLen-len(goodFiles)} files rejected becasue of bad extension',  classes='bg-red-700')
         if len(goodFiles)>0:
            goLabelButton.enable()
         
         

    
    with ui.row().classes(' my-color w-full min-h-screen justify-center p-0 m-0 flex'):

        with ui.column().classes('bg-linear-to-r min-h-screen from-yellow-500  to-amber-500 m-0 w-[40vw] h-full justify-center align-center items-end px-32'):
            ui.html('''
                <div class='text-xl text-black mb-8'>Upload your images here: </div>
            ''')
            ui.upload(on_multi_upload=uploadHandler,  
                      on_rejected=lambda: ui.notify('Rejected!',classes='bg-red-700'),  multiple=True).classes('bg-red-500')\
                      .classes('w-full bg-stone-900 h-[34rem] max-h-[100vh] rounded-lg')
            goLabelButton = ui.button('Label images ', icon='arrow_forward_outline', on_click=lambda: ui.navigate.to(APP_URL+'workspace')).classes('w-full rounded-lg mt-8 bg-white text-black') 
            goLabelButton.disable()

        with ui.column().classes('p-0 pl-64 bg-linear-to-r min-h-screen from-stone-800 to-stone-900 w-[60vw] m-0 justify-center  items-start'):
            ui.html(''' <div class="w-[80%] text-white text-[4rem]  h-full">
            Welcome to 
            <strong class="text-[9rem] mb-0">
                <span class="text-yellow-500  mb-0">Label</span>It<span class="text-yellow-500  mb-0">!</span>
            </strong>
             <br/><div class="text-2xl subtitle -mt-4">Upload images and label your dataset.</div>
            </div>''', sanitize=False)

@ui.page('/workspace')
def homePage():
    basicAppSettings('Worksapce')
    # if len(goodFiles)==0:
    #     ui.navigate.to(APP_URL)
   
    with ui.header().style('background-color: #3874c8').classes('items-center justify-between bg-stone-900').style("""

    background-color: var(--color-stone-900);
"""):
        ui.button(on_click=lambda: left_drawer.toggle(), icon='s_grid_view').props('flat color=white')
        ui.label('LabelIt!')
        ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
        
    with ui.left_drawer(top_corner=True, bottom_corner=True, fixed=False).classes('bg-stone-800').classes('') as left_drawer:
      ui.label('IMAGES').classes('px-6 py-3 w-full justify-center text-center')
    with ui.right_drawer(top_corner=True, bottom_corner=True, fixed=False).classes('bg-stone-800').classes('') as right_drawer:
          ui.label('LABELS').classes('px-6 py-3 w-full justify-center text-center')
    ui.html('''
        <div class="bg-stone-900 w-full h-full">yolo</div>
        ''', sanitize=False)



ui.run()
                