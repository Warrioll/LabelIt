from nicegui import ui, events
from Box import Box
from DatasetImage import DatasetImage
from typeguard import typechecked
import state
from nicegui.events import GenericEventArguments

@typechecked
def imagesDrawer():

    markup='bg-amber-400'
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
                 ui.run_javascript("""

                    const croppedImg=  new fabric.Rect({
                                   id: """+str(box.boxId)+""",
                                   left: """+str(box.position[0])+"""*window.canvasScale,
                                   top: """+str(box.position[1])+"""*window.canvasScale,
                                   width: """+str(box.width)+"""*window.canvasScale,
                                   height: """+str(box.height)+"""*window.canvasScale, 
                                   fill: 'rgba(250, 250, 250, 0.3)',//'rgba(230, 198, 91, 0.3)',
                                   stroke: 'white',//'rgba(219, 166, 84, 1)',
                                   strokeWidth: 2, 
                                   transparentCorners: false,
                                   cornerColor: 'white',
                                   cornerStrokeColor: 'blue',
                                   cornerSize: 10,
                                   lockRotation: true,
                                   hasControls: true,
                                   hasBorders: true
                               }); 
                    window.myCanvas.add(croppedImg);
                    window.myCanvas.renderAll();

                """)

            if not (selectedImgButton is None):
                selectedImgButton.classes(remove=markup)
            selectedImgButton=e.sender
            selectedImgButton.classes(markup)
            state.refreshBoxesList()
            state.refreshClassesList()

    ui.label('IMAGES').classes(' py-3 w-full justify-center text-center')
    with ui.scroll_area().props('dark').classes('h-full'):
        with ui.button_group().props('unelevated'):
            with ui.grid(columns=2):
                for i in range(len(state.files)):
                    with ui.button(on_click=lambda e,im=state.files[i]:setCanvasImg(e,im)).props('flat dense color=amber').classes('p-0 m-1') as btn:
                        if i==0:
                            btn.classes(markup)
                            selectedImgButton=btn
                        ui.image(state.files[i].getPIL()).classes('w-32 h-28 m-1 object-contain')

    