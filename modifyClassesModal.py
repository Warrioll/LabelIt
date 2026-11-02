import state
from nicegui import ui, events

def modifyClassesModal():
    with ui.dialog() as dialog, ui.card().props('dark').classes('w-[50vw] h-[50vh]'):
        with ui.row().classes('w-full relative items-center justify-center p-3 '):
            ui.label('EDIT CLASSES').classes(' text-md font-medium')
            ui.button(icon='close', on_click=dialog.close).classes('absolute right-0').props('flat color=white')
        with ui.scroll_area().props('dark').classes('h-full  mt-3'):
            with ui.list().props('dense separator').classes('w-full justify-between items-center mx-8'):
                with ui.item().classes('uppercase  text-md text-stone-200'):
                    ui.label('Id').classes('  w-full')
                    ui.label('Class name').classes('  w-full')
                for class_name, class_id in list(state.classesList.items()):
                    current_name = {'value': class_name}

                    with ui.item().classes('w-full'):
                        id_input = ui.number(
                            value=class_id,
                            precision=0,
                            placeholder='ID',
                        ).classes('w-24')

                        name_input = ui.input(
                            value=class_name,
                            placeholder='Class name',
                        ).classes('flex-grow')

                        def update_id(e, name=current_name):
                            if e.value is not None:
                                state.classesList[name['value']] = int(e.value)

                        def update_name(e, name=current_name):
                            new_name = e.value.strip()
                            old_name = name['value']

                            if not new_name or new_name == old_name:
                                return

                            if new_name in state.classesList:
                                ui.notify('Ta nazwa już istnieje!', type='warning')
                                return

                            class_id = state.classesList.pop(old_name)
                            state.classesList[new_name] = class_id

                            name['value'] = new_name

                        id_input.on_value_change(update_id)
                        name_input.on_value_change(update_name)
                
        with ui.row().classes('w-full items-center justify-center p-3 '):
            ui.button('Add class',icon='add', on_click=dialog.close).props('flat color=amber dense').classes('items-center normal-case w-full')

    ui.button('Edit classes', on_click=dialog.open).props('flat color=amber')

