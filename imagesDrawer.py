from nicegui import ui, events
from Box import Box
from DatasetImage import DatasetImage
from typeguard import typechecked
import state
from nicegui.events import GenericEventArguments
import utils

@typechecked
def imagesDrawer():

    markup='bg-amber-400 text-stone-900'
    selectedImgButton:ui.button|None=None
    def setCanvasImg(e: GenericEventArguments,img: DatasetImage):
            nonlocal selectedImgButton
            state.currentImg=img
            state.refreshFooter()
            imgW, imgH = state.currentImg.getImageSize()

            ui.run_javascript("""

                window.canvasScale=Math.min(window.maxCanvasHeight/"""+str(imgH)+""", window.maxCanvasWidth/"""+str(imgW)+""")
            
                window.myCanvas.getObjects('rect').forEach(rect => {
                    window.myCanvas.remove(rect);
                });

                window.setCanvasImg('"""+state.currentImg.getUrl()+"""', window.canvasScale, """+str(imgW)+""", """+str(imgH)+""")
            """)

            box:Box
            for box in state.currentImg.boxes:
                #  ui.run_javascript("""

                #     const croppedImg=  new fabric.Rect({
                #                    id: """+str(box.boxId)+""",
                #                    left: """+str(box.position[0])+"""*window.canvasScale,
                #                    top: """+str(box.position[1])+"""*window.canvasScale,
                #                    width: """+str(box.width)+"""*window.canvasScale,
                #                    height: """+str(box.height)+"""*window.canvasScale, 
                #                    fill: 'rgba(250, 250, 250, 0.3)',//'rgba(230, 198, 91, 0.3)',
                #                    stroke: 'white',//'rgba(219, 166, 84, 1)',
                #                    strokeWidth: 2, 
                #                    transparentCorners: false,
                #                    cornerColor: 'white',
                #                    cornerStrokeColor: 'blue',
                #                    cornerSize: 10,
                #                    lockRotation: true,
                #                    hasControls: true,
                #                    hasBorders: true
                #                }); 
                #     window.myCanvas.add(croppedImg);
                #     window.myCanvas.renderAll();

                # """)
                utils.drawBox(box.boxId,box.position[0],box.position[1],box.width,box.height, box.labelClass.color['value'])

            if not (selectedImgButton is None):
                selectedImgButton.classes(remove=markup)
                elements = selectedImgButton.descendants()
                label = next((el for el in elements  if isinstance(el, ui.label)), None)
                label.classes(remove='text-stone-900')
                label.classes(add='text-amber-400')
            selectedImgButton=e.sender
            selectedImgButton.classes(markup)
            elements = selectedImgButton.descendants()
            label = next((el for el in elements  if isinstance(el, ui.label)), None)
            label.classes(add='text-stone-900')
            state.refreshBoxesList()
            state.refreshClassesList()

    ui.label('IMAGES').classes(' py-3 w-full justify-center text-center')
    with ui.scroll_area().props('dark').classes('h-full'):
        with ui.button_group().props('unelevated'):
            with ui.grid(columns=2):
                for i in range(len(state.files)):
                    with ui.button(on_click=lambda e,im=state.files[i]:setCanvasImg(e,im)).props('flat dense color=amber').classes('p-0 m-1') as btn:
                                    

                        
                        ui.image(state.files[i].getPIL()).classes('w-32 h-20 m-1 object-contain')
                        label = ui.label(state.files[i].name).classes('w-full break-all no-caps text-left mx-2 mb-1 text-xs text-amber-400')

                        if i==0:
                            btn.classes(markup)
                            selectedImgButton=btn 
                            label.classes(add='text-stone-900')        

                        # @ui.refreshable
                        # def label(btn=btn):
                        #     if btn==selectedImgButton:
                        #         ui.label(state.files[i].name).classes('w-full break-all no-caps text-left mx-2 mb-2 text-xs text-stone-900')
                        #     else:
                        #         ui.label(state.files[i].name).classes('w-full break-all no-caps text-left mx-2 mb-2 text-xs text-amber-400')
                        # label()

                        @ui.refreshable
                        def badge(index=i):
                                bd= ui.badge(state.files[index].status).props('floating dense ')
                                if state.files[index].status=='Done':
                                    bd.set_background_color('forestgreen')
                                    bd.set_text_color('white')
                                elif state.files[index].status=='Review':
                                     bd.set_background_color('blue')
                                     bd.set_text_color('white')
                                else:
                                      bd.set_background_color('white')
                                      bd.set_text_color('black')
                        state.files[i].refreshBadge=badge.refresh
                        badge()

    