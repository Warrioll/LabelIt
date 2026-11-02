from nicegui import ui, events
from Box import Box
from typeguard import typechecked
from DatasetImage import DatasetImage
import state

@typechecked
def labelsDrawer():

    selectedLabel:ui.item | None = None
    selectedLabelBoxId:int|None =None

    markup='bg-amber-500/20'
    def markLabelHander( boxId:int):
        nonlocal selectedLabelBoxId
        # nonlocal selectedLabel
        # if not (selectedLabel is None):
        #       selectedLabel.classes(remove=markup)
        # selectedLabel=sender
        # selectedLabel.classes(markup)
        selectedLabelBoxId=boxId
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

    ui.on('boxMarked',boxMarkedHandler)

    @ui.refreshable
    def boxesListFun():
             with ui.list().props('dense separator').classes('w-full '):
                for i in range(len(state.currentImg.boxes)):
                    with ui.item(on_click=lambda e, boxId=state.currentImg.boxes[i].boxId: markLabelHander( boxId)).classes(' px-4 items-center').classes('w-full ') as itm: 
                        with ui.item_section().classes('w-6 ').props('side'):
                            no = ui.label(str(i+1)+'.')
                        with ui.item_section().classes('col min-w-0'):
                            sel = ui.select(options=list(state.classesList.keys()), value=state.currentImg.boxes[i].className,with_input=False,on_change=lambda e: state.currentImg.boxes[i].changeClassName(e.value)).classes('w-full ').props(
                                'dark dense filled color=amber options-dense')
                        with ui.item_section().classes('shrink-0').props('side'):
                            delBtn= ui.button(icon='delete_outline').props('dense dark flat color=amber').classes('shrink-0 q-ma-none q-pa-none')
                        if state.currentImg.boxes[i].boxId==selectedLabelBoxId:
                                                     itm.classes(markup)
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