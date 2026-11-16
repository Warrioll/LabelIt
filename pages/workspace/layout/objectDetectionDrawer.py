from nicegui import ui
from typeguard import typechecked
import state
import pages.workspace.canvas as canvas

@typechecked
def objectDetectionDrawer():

    markup='bg-amber-500/20'
    def markLabelHander( boxId:str):
        state.selectedLabelBoxId=boxId
        state.refreshBoxesList()

        canvas.markBox(boxId)

    def boxMarkedHandler(e):
        markLabelHander(e.args["boxId"])

    def deleteLabel(boxId:str):
        box = next((b for b in state.currentImg.boxes if b.boxId == boxId), None)

        if box is not None:
            state.currentImg.boxes.remove(box)
            del box
        canvas.eraseBox(boxId)
        state.refreshBoxesList()

    ui.on('boxMarked',boxMarkedHandler)

    @ui.refreshable
    def boxesListFun():


             with ui.list().props('dense separator').classes('w-full '):
                for i in range(len(state.currentImg.boxes)):
                    with ui.item().classes(' px-4 items-center').classes('w-full ').style("""  border-left: 3px solid """+state.currentImg.boxes[i].labelClass.color['value']+"""; """) as itm: 
                        
                        with ui.item_section().classes('w-6 ').props('side'):
                            no = ui.label(str(i+1)+'.')
                        
                        with ui.item_section().classes('shrink-0').props('side'):
                            with ui.button(icon='crop',on_click=lambda e, boxId=state.currentImg.boxes[i].boxId: markLabelHander( boxId)). props('dense flat color=amber').classes('q-ma-none q-pa-none'):
                                   ui.tooltip('Change selection').classes('text-xs bg-stone-900 text-center')
                        
                        with ui.item_section().classes('col min-w-0'):
                                def changeLabelClassHandler(e, obj=state.currentImg.boxes[i]):
                                    obj.changeClassName( state.classesList.getClassByName(e.value))
                                    canvas.eraseBox(obj.boxId)
                                    canvas.drawBox(obj.boxId, obj.position[0], obj.position[1], obj.width, obj.height,obj.labelClass.color['value'])
                                    state.refreshBoxesList()

                                      
                                with ui.select(
                                    options=state.classesList.getClassesNames(),
                                    value=state.currentImg.boxes[i].labelClass.className,
                                    with_input=False,
                                    on_change=changeLabelClassHandler
                                ).classes('w-full min-w-0 truncate').props('dark dense filled color=amber options-dense ').style('max-width: 10.1rem;'):
                                   ui.tooltip('Set class').classes('text-xs bg-stone-900 text-center')
                        
                        with ui.item_section().classes('shrink-0').props('side'): 
                            with ui.button(icon='delete_outline', on_click=lambda boxId=state.currentImg.boxes[i].boxId: deleteLabel(boxId)).props('dense dark flat color=amber').classes('shrink-0 q-ma-none q-pa-none'):
                                   ui.tooltip('Delete label').classes('text-xs bg-stone-900 text-center')
                        if state.currentImg.boxes[i].boxId==state.selectedLabelBoxId:
                                                     itm.classes(markup)
                                                     no.classes('text-white')
                                                     #no.classes('text-amber-400')
                                                    #  delBtn.props('color=stone')
                                                    #  sel.props('color=stone')

    state.refreshBoxesList=boxesListFun.refresh
 

    ui.on('boxCreated', boxesListFun.refresh)

    ui.label('LABELS').classes('px-6 py-3 w-full justify-center text-center')
    with ui.scroll_area().props('dark').classes('h-full'):
                     #boxesList = ui.column()
                    #  for box in boxes:
                    #       ui.label(box.boxId).move(updateBoxesList)
            boxesListFun()