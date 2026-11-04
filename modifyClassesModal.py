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
                        ui.label('Id').classes('w-28 shrink-0 ml-4')
                        ui.label('Class name').classes('flex-grow min-w-0 ml-6')

                    # Wiersze
                    classesData=[ [c.classId, c.className] for c in state.classesList.classes]

                    for i, labelClass in enumerate(state.classesList.classes):

                        with ui.item().classes('w-full items-start no-wrap'):
                        
                            def validateId(value, obj=labelClass):
                                if value is None:
                                    return 'Invalid Id'

                                if not state.classesList.checkIfClassIdAvailable(int(value), obj):
                                    return ''#f'This class id is already assigned ({value})!'

                                return None

                            def validateName(value, obj=labelClass):
                                if not value:
                                    return 'Invalid name'

                                if not state.classesList.checkIfClassNameAvailable(value, obj):
                                    return ''#f'This class name is already assigned ({value})!'

                                return None

                            def numberChangeHandler(e, obj=labelClass, index=i):
                                classId = int(e.value)
                                classesData[index][0] = classId

                                if validateId(classId, obj) is None:
                                    obj.classId = classId
                                    state.refreshBoxesList()
                                else:
                                    ui.notify(f'This class id is already assigned ({classId})!',type='negative', icon='error')

                            def nameChangeHandler(e, obj=labelClass, index=i):
                                className = e.value
                                classesData[index][1] = className

                                if validateName(className, obj) is None:
                                    obj.className = className
                                    state.refreshBoxesList()
                                else:
                                    ui.notify(f'This class name is already assigned ({className})!',  type='negative', icon='error')

                            ui.number(
                                value=classesData[i][0],
                                precision=0,
                                format='%.f',
                                validation=validateId,
                                on_change=numberChangeHandler
                            ).classes('w-28 mx-3 shrink-0 self-center').props('dark filled dense color=amber')

                            ui.input(
                                value=classesData[i][1],
                                validation=validateName,
                                on_change=nameChangeHandler
                            ).classes('col min-w-0 mx-3 self-center').props('dark filled dense color=amber')

                            ui.button(icon='delete_outline') \
                                .props('dense dark flat color=amber') \
                                .classes('shrink-0 q-ma-none q-pa-none mx-3 mt-2')

            with ui.row().classes('w-full items-center justify-center p-3'):
                ui.button(
                    'Add class',
                    icon='add',
                    on_click=dialog.close
                ).props('flat color=amber dense').classes('normal-case w-full')

    ui.button('Edit classes', on_click=dialog.open).props('flat color=amber')
