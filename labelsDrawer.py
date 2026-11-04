from nicegui import ui, events
from Box import Box
from typeguard import typechecked
from DatasetImage import DatasetImage
import state

@typechecked
def labelsDrawer():

    selectedLabel:ui.item | None = None
    #selectedLabelBoxId:int|None =None

    markup='bg-amber-500/20'
    def markLabelHander( boxId:int):
        # nonlocal selectedLabelBoxId
        # nonlocal selectedLabel
        # if not (selectedLabel is None):
        #       selectedLabel.classes(remove=markup)
        # selectedLabel=sender
        # selectedLabel.classes(markup)
        state.selectedLabelBoxId=boxId
        state.refreshBoxesList()

        ui.run_javascript("""
            const rect = window.myCanvas.getObjects().find(obj => obj.id === """+str(boxId)+""");

            if (rect) {
                window.myCanvas.setActiveObject(rect);
                window.myCanvas.requestRenderAll();
            }
        """)

    def boxMarkedHandler(e):
        markLabelHander(int(e.args["boxId"]))

    def deleteLabel(boxId:int):
        box = next((b for b in state.currentImg.boxes if b.boxId == boxId), None)

        if box is not None:
            state.currentImg.boxes.remove(box)
            del box
        ui.run_javascript("""
            const rect = window.myCanvas.getObjects().find(obj => obj.id === """+str(boxId)+""");

            if (rect) {
                window.myCanvas.remove(rect);
                window.myCanvas.requestRenderAll();
            }
        """)
        state.refreshBoxesList()

    ui.on('boxMarked',boxMarkedHandler)

    @ui.refreshable
    def boxesListFun():
             with ui.list().props('dense separator').classes('w-full '):
                for i in range(len(state.currentImg.boxes)):
                    with ui.item().classes(' px-4 items-center').classes('w-full ') as itm: 
                        
                        with ui.item_section().classes('w-6 ').props('side'):
                            no = ui.label(str(i+1)+'.')
                        
                        with ui.item_section().classes('shrink-0').props('side'):
                            with ui.button(icon='crop',on_click=lambda e, boxId=state.currentImg.boxes[i].boxId: markLabelHander( boxId)). props('dense flat color=amber').classes('q-ma-none q-pa-none'):
                                   ui.tooltip('Change selection').classes('text-xs bg-stone-900 text-center')
                        
                        with ui.item_section().classes('col min-w-0'):
                            with ui.select(options=state.classesList.getClassesNames(), value=state.currentImg.boxes[i].labelClass.className,with_input=False,on_change=lambda e: state.currentImg.boxes[i].changeClassName(state.classesList.getClassByName(e.value))).classes('w-full ').props(
                                'dark dense filled color=amber options-dense'):
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