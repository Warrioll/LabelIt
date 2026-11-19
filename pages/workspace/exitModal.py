from nicegui import ui
import state

def exitModal():

    # def clearProject():
    #      state.files.clear()
    #      state.currentImg=None
    #      state.selectedLabelBoxId =None

    #      state.classesList.clearLabelClassesList()
         
    #      state.imagesClassesList.clearImageClassesList()
    #      state.classesCounter=0
    #      ui.run_javascript('window.location.reload()')

    with ui.dialog().props('backdrop-filter="blur(8px) brightness(200%) contrast(30%)" ') as dialog:
            with ui.card().props('dark').classes('w-160 h-92 max-w-none shadow-none bg-stone-900'):
                with ui.row().classes('w-full relative items-center justify-center p-3'):
                    
                    ui.button(icon='close', on_click=dialog.close) \
                        .classes('absolute right-0').props('flat color=amber').classes('pt-5')
                with ui.element('div').classes('w-full h-full p-8 flex flex-col justify-center items-center'):
                    ui.label('Are you sure you want to clear all data? ').classes('text-2xl font-bold text-center w-full mb-8')
                    ui.label('This will permanently delete all uploaded images, labels, and annotations.').classes('text-lg font-medium text-center w-full mb-8')
                    with ui.row().classes('justify-center shadow-none mt-8'):
                         ui.button('Yes', on_click=state.clearProject).props('color=red outline').classes('w-40 mx-8')
                         ui.button('Cancel',on_click=dialog.close).classes('w-40 mx-8').props('color=amber text-color=stone-900 ')
                
    
    
    ui.button('Clear ', on_click=dialog.open).props('flat color=red no-caps')