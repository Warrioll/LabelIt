from nicegui import ui, events
from Box import Box
from typeguard import typechecked
from DatasetImage import DatasetImage
import state
from ImageClass import ImageClass

def imageRecognitionDrawer():

    markup='bg-amber-500/20'

    def classAssigementHandler(e, obj:ImageClass):
        if e.value:
                  if not( obj in state.currentImg.imageClasses):
                          state.currentImg.appendClass(obj)
        else:
               if obj in state.currentImg.imageClasses:
                      state.currentImg.removeClass(obj)
        e.sender.set_value(e.value)
        state.refreshClassesList()
                         

    @ui.refreshable
    def classesListFun():
             with ui.list().props('dense separator').classes('w-full '):
                for i in range(len(state.imagesClassesList.classes)):
                    with ui.item().classes(' px-4 items-center').classes('w-full ') as itm: 
                        
                        with ui.item_section().classes('w-6 ').props('side'):
                            no = ui.label(str(i+1)+'.')
                        
                        with ui.item_section().classes('shrink-0 ml-1').props('side'):
                                obj = state.imagesClassesList.classes[i]

                                with ui.checkbox(
                                        value=obj in state.currentImg.imageClasses,
                                        on_change=lambda e, obj=obj: classAssigementHandler(e, obj)).props('dark color=amber'):
                                        ui.tooltip('Assign class to image').classes('text-xs bg-stone-900 text-center')
                        
                        with ui.item_section().classes('col min-w-0 ml-0'):
                           ui.label(state.imagesClassesList.classes[i].className).classes('truncate w-full min-w-0').style('max-width: 12rem')                        
                        if state.imagesClassesList.classes[i] in state.currentImg.imageClasses:
                                                     itm.classes(markup)
                                                     no.classes('text-white')
                                                     #no.classes('text-amber-400')
                                                    #  delBtn.props('color=stone')
                                                    #  sel.props('color=stone')

    state.refreshClassesList=classesListFun.refresh
 

    ui.label('CLASSES').classes('px-6 py-3 w-full justify-center text-center')
    with ui.scroll_area().props('dark').classes('h-full'):
                     #boxesList = ui.column()
                    #  for box in boxes:
                    #       ui.label(box.boxId).move(updateBoxesList)
            classesListFun()
