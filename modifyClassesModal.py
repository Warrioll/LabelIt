import state
from nicegui import ui


def modifyClassesModal():
    with ui.dialog() as dialog:
        with ui.card().props('dark').classes('w-[50vw] h-[50vh] max-w-none'):

            with ui.row().classes('w-full relative items-center justify-center p-3'):
                ui.label('EDIT CLASSES').classes('text-md font-medium')
                ui.button(icon='close', on_click=dialog.close) \
                    .classes('absolute right-0').props('flat color=white')

            with ui.scroll_area().classes('w-full flex-grow min-h-0 mt-3 px-4'):
                with ui.list().props('dense separator').classes('w-full'):

                    # Nagłówek
                    with ui.item().classes('w-full items-center no-wrap'):
                        ui.label('ID').classes('w-20 shrink-0')
                        ui.label('Class name').classes('flex-grow min-w-0')

                    # Wiersze
                    for labelClass in state.classesList.classes:
                        with ui.item().classes('w-full items-center no-wrap'):
                            ui.number(
                                placeholder='ID',
                                precision=0,
                                value=labelClass.classId,
                                format='%.f',
                                on_change=lambda e, lc=labelClass: lc.setClassId(int(e.value))
                            ).classes('w-16 mx-3 shrink-0 self-center').props('dark filled dense color=amber')

                            ui.input(
                                value=labelClass.className,
                                placeholder='Class name',
                            ).classes('col min-w-0 mx-3 self-center ').props('dark filled dense color=amber')

                            ui.button(icon='check') \
                                .props('dense dark flat color=amber') \
                                .classes('shrink-0 q-ma-none q-pa-none mx-3 self-center')

                            ui.button(icon='delete_outline') \
                                .props('dense dark flat color=amber') \
                                .classes('shrink-0 q-ma-none q-pa-none mx-3 self-center')

            with ui.row().classes('w-full items-center justify-center p-3'):
                ui.button(
                    'Add class',
                    icon='add',
                    on_click=dialog.close
                ).props('flat color=amber dense').classes('normal-case w-full')

    ui.button('Edit classes', on_click=dialog.open).props('flat color=amber')