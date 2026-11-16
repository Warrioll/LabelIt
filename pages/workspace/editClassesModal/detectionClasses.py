import state
from nicegui import ui
import pages.workspace.canvas as canvas

def detectionClasses():

    @ui.refreshable
    def displayClassesList():
        classesData = [[c.classId, c.className] for c in state.classesList.classes]

        for i, labelClass in enumerate(state.classesList.classes):

            with ui.item().classes('w-full items-start no-wrap pt-2 pb-5'):

                def validateId(value, obj=labelClass):
                    if value is None:
                        ui.notify('Invalid Id', type='negative', icon='error')
                        return ''

                    if not state.classesList.checkIfClassIdAvailable(int(value), obj):
                        return ''

                    return None

                def validateName(value, obj=labelClass):
                    if not value:
                        ui.notify('Invalid name', type='negative', icon='error')
                        return ''

                    if not state.classesList.checkIfClassNameAvailable(value, obj):
                        return ''

                    return None

                def numberChangeHandler(e, obj=labelClass, index=i):
                    if e.value is not None:
                        classId = int(e.value)
                        classesData[index][0] = classId

                        if validateId(classId, obj) is None:
                            obj.classId = classId
                            state.refreshBoxesList()
                        else:
                            ui.notify(
                                f'This class id is already assigned ({classId})!',
                                type='negative',
                                icon='error'
                            )

                def nameChangeHandler(e, obj=labelClass, index=i):
                    className = e.value
                    classesData[index][1] = className

                    if validateName(className, obj) is None:
                        obj.className = className
                        state.refreshBoxesList()
                    else:
                        ui.notify(
                            f'This class name is already assigned ({className})!',
                            type='negative',
                            icon='error'
                        )

                ui.number(
                    value=classesData[i][0],
                    precision=0,
                    format='%.f',
                    validation=validateId,
                    on_change=numberChangeHandler
                ).classes('w-28 mx-3 shrink-0 self-center p-0').props(
                    'dark filled dense color=amber'
                )

                # COLOR PICKER
                selectedColor = labelClass.color
                with ui.button().props(' flat  color=amber dense').classes(
                    'shrink-0 w-8 h-8 mt-1 mx-5' ).style( f''' background-color: {selectedColor["value"]} !important;''') as colorButton:
                    ui.tooltip('Change class color').classes('text-xs bg-stone-800 text-center')

                    def updateColor(color, btn=colorButton, obj=labelClass):
                        obj.color = color
                    
                        btn.style(
                            f'background-color: {color["value"]} !important;'
                        )
                    
                        state.refreshBoxesList()
                        canvas.eraseAllBoxes()
                        canvas.drawAllCurrrentImgBoxes()
                    
                    with ui.menu().props('dark').classes('shadow-none bg-stone-800 border-1 border-stone-700') as colorMenu:
                        with ui.grid(columns=5).classes('gap-2 p-2'):
                            for color in state.labelColors:
                            
                                def selectColor(
                                    c=color,
                                    menu=colorMenu,
                                    update=updateColor
                                ):
                                    update(c)
                                    menu.close()
                    
                                ui.button(
                                    on_click=selectColor
                                ).props('flat color=amber dense').classes(
                                    'w-8 h-8 m-1'
                                ).style(
                                    f'background-color: {color["value"]} !important;'
                                )
                    
                                        

                ui.input(
                    value=classesData[i][1],
                    validation=validateName,
                    on_change=nameChangeHandler
                ).classes('col min-w-0 mx-3 self-center p-0').props(
                    'dark filled dense color=amber'
                )

                with ui.button(
                    icon='delete_outline',
                    on_click=lambda innerId=labelClass.innerId: deleteClass(innerId)
                ).props('dense dark flat color=amber').classes(
                    'shrink-0 q-ma-none q-pa-none mx-3 mt-2'
                ):
                    ui.tooltip('Delete class').classes('text-xs bg-stone-800 text-center')

    def addNewClass():
        state.classesList.addNewClass()
        displayClassesList.refresh()
        state.refreshBoxesList()

    def deleteClass(classInnerId):
        labelClass = next(
            (c for c in state.classesList.classes if classInnerId == c.innerId),
            None
        )

        if labelClass is not None:
            innerIdToDel = labelClass.innerId
            state.classesList.classes.remove(labelClass)
            del labelClass

            for img in state.files:
                for box in img.boxes:
                    if box.labelClass.innerId == innerIdToDel:
                        box.labelClass = state.classesList.nonClass

            ui.notify(
                'Class deleted. Please reassign the affected labels to another class.',
                classes='bg-white text-black'
            )

            if len(state.classesList.classes) == 0:
                state.classesList.addNewClass()
                ui.notify(
                    'All object detection classes have been deleted. A default class has been added to ensure that at least one class exists.',
                    classes='bg-white text-black'
                )

            displayClassesList.refresh()
            state.refreshBoxesList()

    with ui.scroll_area().classes('w-full flex-grow min-h-0 mt-3 px-4').props('dark'):
        with ui.list().props('dense separator').classes('w-full'):

            # Nagłówek
            with ui.item().classes('w-full items-center no-wrap'):
                ui.label('Id').classes('w-28 shrink-0 ml-4')
                ui.label('Color').classes('w-10 shrink-0 ml-7')
                ui.label('Class name').classes('flex-grow min-w-0 ml-6')

            # Wiersze
            displayClassesList()

    with ui.row().classes('w-full items-center justify-center p-3'):
        ui.button(
            'Add class',
            icon='add',
            on_click=addNewClass
        ).props('flat color=amber dense').classes('normal-case w-full')