import state
from nicegui import ui
from pages.workspace.editClassesModal.detectionClasses import detectionClasses
from pages.workspace.editClassesModal.recognitionClasses import recognitionClasses


def editClassesModal():



    with ui.dialog().props('backdrop-filter="blur(8px) brightness(200%) contrast(30%)" ') as dialog:
        with ui.card().props('dark').classes('w-[50vw] h-[70vh] max-w-none shadow-none bg-stone-900'):

            with ui.row().classes('w-full relative items-center justify-center p-3'):
                ui.label('EDIT CLASSES').classes('text-md font-medium')
                ui.button(icon='close', on_click=dialog.close) \
                    .classes('absolute right-0').props('flat color=amber')
            with ui.tabs().classes('w-full').props('dense color=amber indicator-color=amber active-color=amber') as tabs:
                one = ui.tab('Object detection').classes('whitespace-normal w-full').props('color=amber no-caps')
                two = ui.tab('Image recognition').classes('whitespace-normal w-full').props('color=amber no-caps')
            with ui.tab_panels(tabs, value=one).classes('w-full h-full bg-stone-900').props('dark'):
                with ui.tab_panel(one):
                    detectionClasses()
                with ui.tab_panel(two):
                    recognitionClasses()
            


    ui.button('Classes', on_click=dialog.open).props('flat color=amber no-caps')
