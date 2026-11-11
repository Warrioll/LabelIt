import state
from nicegui import ui

def recognitionClasses():

    @ui.refreshable
    def displayClassesList():
                    classesData=[  c.className for c in state.imagesClassesList.classes]

                    for i, recognitionClass in enumerate(state.imagesClassesList.classes):

                        with ui.item().classes('w-full items-start no-wrap pt-2 pb-5'):

                            # def validateName(value, index=i):
                            #     if not value:
                            #         ui.notify('Invalid name',type='negative', icon='error')
                            #         return ''
                                
                            #     if state.imagesClassesList.checkIfClassNameAvailable(value,state.imagesClassesList.classes[index]):
                            #          return None
                            #     else: return ''

                            def validateName(value, obj=recognitionClass):
                                if not value:
                                    ui.notify('Invalid name',type='negative', icon='error')
                                    return ''
                                       
                                if not state.imagesClassesList.checkIfClassNameAvailable(value, obj):
                                    return ''#f'This class name is already assigned ({value})!'

                                return None
                                     
                                
                            def nameChangeHandler(e, obj=recognitionClass, index=i):
                                className = e.value
                                classesData[index] = className

                                if validateName(className, obj) is None:
                                    obj.className = className

                                    state.refreshClassesList()
                                else:
                                    ui.notify(f'This class name is already assigned ({className})!',  type='negative', icon='error')

                            ui.input(
                                value=state.imagesClassesList.classes[i].className,
                                validation=validateName,
                                on_change=nameChangeHandler
                            ).classes('col min-w-0 mx-3 self-center p-0').props('dark filled dense color=amber')

                            with ui.button(icon='delete_outline', on_click=lambda innerId=recognitionClass.innerId: deleteClass(innerId)) \
                                                            .props('dense dark flat color=amber') \
                                                            .classes('shrink-0 q-ma-none q-pa-none mx-3 mt-2'):
                                  ui.tooltip('Delete class').classes('text-xs bg-stone-800 text-center')

    def addNewClass():
            state.imagesClassesList.addNewClass()
            displayClassesList.refresh()
            #TODO
            state.refreshClassesList()

    def deleteClass(classInnerId):
            imageClass= next((c for c in state.imagesClassesList.classes if classInnerId== c.innerId), None)
            print(classInnerId, imageClass)
            if imageClass is not None:
                         innerIdToDel=imageClass.innerId
                         state.imagesClassesList.classes.remove(imageClass)
                         
                         for img in state.files:
                              for cls in img.imageClasses:
                                   if cls.innerId==innerIdToDel:
                                        img.imageClasses.remove(imageClass)
                         del imageClass
                         ui.notify('Class deleted. Please reassign the affected labels to another class.', classes='bg-white text-black')
                         if len(state.imagesClassesList.classes)==0:
                              state.imagesClassesList.addNewClass()
                              ui.notify('All object detection classes have been deleted. A default class has been added to ensure that at least one class exists.', classes='bg-white text-black')
                         displayClassesList.refresh()
                         #TODO
                         state.refreshClassesList()

    with ui.scroll_area().classes('w-full flex-grow min-h-0 mt-3 px-4').props('dark '):
        with ui.list().props('dense separator').classes('w-full'):
            # Nagłówek
            with ui.item().classes('w-full items-center no-wrap'):
                # ui.label('Id').classes('w-28 shrink-0 ml-4')
                ui.label('Class name').classes('flex-grow min-w-0 ml-6')
            # Wiersze
            displayClassesList()
            
    with ui.row().classes('w-full items-center justify-center p-3'):
        ui.button(
            'Add class',
            icon='add',
            on_click=addNewClass
        ).props('flat color=amber dense').classes('normal-case w-full')