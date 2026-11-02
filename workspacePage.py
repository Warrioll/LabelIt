from nicegui import ui, events
from utils import basicAppSettings
from PIL import Image
from DatasetImage import DatasetImage
from pathlib import Path
from Box import Box
from labelsDrawer import  labelsDrawer
from imagesDrawer import imagesDrawer
import state
from modifyClassesModal import modifyClassesModal

def workspacePage():
    print('Worksapce')
    basicAppSettings('Worksapce')
    # if len(files)==0:
    #     ui.navigate.to('/')

    ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/fabric@5/dist/fabric.min.js"></script>')

    maxCanvasWidth=1200.0
    maxCanvasHeight=860.0
    

    def cerateCanvas():

        ui.run_javascript("""                        
            const el = document.getElementById('myCanvas');
            if (!el) {
                console.log('Nie znaleziono canvasu')
                return 'Nie znaleziono canvasu';
                }
                
            if (el.dataset.fabricInitialized === 'true') return;
            if (typeof window.fabric === 'undefined') {
                    console.log('Fabric.js nie jest załadowany')
                    return 'Fabric.js nie jest załadowany';
                    }

            el.width="""+str(state.currentImg.getImageSize()[0])+"""*window.canvasScale
            el.height="""+str(state.currentImg.getImageSize()[1])+"""*window.canvasScale

            window.myCanvas=  new window.fabric.Canvas(el, {
                selection: false,     
                skipTargetFind: false,
                
                });
            el.dataset.fabricInitialized = 'true';
            window.setCanvasImg=(imgUrl, scale)=>{
                fabric.Image.fromURL(imgUrl, function(img) {
                    window.myCanvas.setBackgroundImage(img, window.myCanvas.renderAll.bind(window.myCanvas), {
                        scaleX: scale,
                        scaleY: scale,
                        });
                    });
                }
            window.rectPreview=null
            window.setCanvasImg('"""+state.currentImg.getUrl()+"""',window.canvasScale)
         """)

        createMouseDownEvent()
        createMouseUpEvent()
        createMouseMoveEvent()
        createModifiedBoxEvent()

    def createMouseDownEvent():
        ui.run_javascript("""
        window.myCanvas.on('mouse:down', function(opt) {
                    if (!opt.target) {
                        const pointer = window.myCanvas.getPointer(opt.e);

                        window.rectPreview= new fabric.Rect({
                            left:  pointer.x,
                            top:  pointer.y,
                            width: 1,
                            height: 1,
                            fill: 'rgba(0, 150, 255, 0.2)',
                            stroke: 'blue',
                            strokeWidth: 2,
                            selectable: false,
                            evented: false,
                        });
                        window.myCanvas.add(window.rectPreview);
                        window.startRect={
                         x: pointer.x,
                         y: pointer.y
                        }
                    }

                    if (opt.target && opt.target.type === 'rect') {
                        emitEvent('boxMarked', {
                            boxId: opt.target.id
                        });
                    }
                });
        
        """)

    def createMouseUpEvent():
        ui.run_javascript("""
        window.myCanvas.on('mouse:up', function(opt) {
            if (!opt.target && window.rectPreview) {
                window.myCanvas.remove(window.rectPreview);
                const pointer = window.myCanvas.getPointer(opt.e);
                window.rectPreview=null

            const left =      Math.min(window.startRect.x, pointer.x)
            const top =    Math.min(window.startRect.y, pointer.y)
            const width = Math.abs(window.startRect.x - pointer.x)
            const height = Math.abs(window.startRect.y - pointer.y)
            const boxId=window.boxCounter
            window.boxCounter++

            if (!(Math.floor(width)===0 && Math.floor(height)===0)){  
                const box=  new fabric.Rect({
                           id: boxId,
                           left:  left,
                            top: top,
                            width: width,
                            height: height,
                           fill: 'rgba(0, 150, 255, 0.3)',
                           stroke: 'blue',
                           strokeWidth: 2, 
                           transparentCorners: false,
                           cornerColor: 'white',
                           cornerStrokeColor: 'blue',
                           cornerSize: 10,
                           lockRotation: true,
                           hasControls: true,
                           hasBorders: true
                       }); 
                      box.setControlsVisibility({
                           mtr: false
                       }); 
                       window.myCanvas.add(box);
                       window.myCanvas.renderAll();

                
                emitEvent('boxCreated', {
                        boxId: boxId,
                        left:  left/window.canvasScale,
                        top: top/window.canvasScale,
                        width: width/window.canvasScale,
                        height: height/window.canvasScale,
                    });
            }
            }
            
        });


        

        """)

    def createMouseMoveEvent():
        ui.run_javascript("""
                window.myCanvas.on('mouse:move', function(opt) {
                    if (!opt.target && window.rectPreview) {
                        const pointer = window.myCanvas.getPointer(opt.e);
                        window.rectPreview.set({
                            left:  Math.min(window.startRect.x, pointer.x),
                            top: Math.min(window.startRect.y, pointer.y),
                            width: Math.abs(window.startRect.x - pointer.x),
                            height: Math.abs(window.startRect.y - pointer.y),
                            });
                        window.myCanvas.requestRenderAll();
                    }
                    
                });
                
                """)
        
    
    def createModifiedBoxEvent(): 
        ui.run_javascript("""
            window.myCanvas.on('object:modified', (opt) => {
                const box = opt.target;

                 box.set({
                    width: box.width * box.scaleX,
                    height: box.height * box.scaleY,
                    scaleX: 1,
                    scaleY: 1
                });

                emitEvent('boxModified', {
                    boxId: box.id,
                    left: box.left/window.canvasScale,
                    top: box.top/window.canvasScale,
                    width: box.width/window.canvasScale,
                    height: box.height/window.canvasScale
                });
            });
        """)



    def boxModifiedHandelr(e):
        box = next((b for b in state.currentImg.boxes if b.boxId == int(e.args["boxId"])), None)
        print(e.args["boxId"])
        if not(box is None):
            print('finded')
            box.position=(float(e.args["left"]), float(e.args["top"]))
            box.width=float(e.args["width"])
            box.height=float(e.args["height"])
        print('modifff!', e.args)
 
    def createBox(e):
        #nonlocal boxCounter
        state.currentImg.appendBox(Box(e.args["boxId"], (e.args["left"], e.args["top"]), e.args["width"],e.args["height"], className=next(iter(state.classesList))))
        print('new Box:',(e.args["left"], e.args["top"]), e.args["width"],e.args["height"])
        #boxCounter+=1


    state.currentImg=state.files[0]
    for img in state.files:
        img.boxes.clear()
    imgW, imgH = state.currentImg.getImageSize()

    ui.run_javascript("""
        window.maxCanvasHeight="""+str(maxCanvasHeight)+""" 
        window.maxCanvasWidth="""+str(maxCanvasWidth)+"""     
        window.canvasScale=Math.min(window.maxCanvasHeight/"""+str(imgH)+""", window.maxCanvasWidth/"""+str(imgW)+""")
        window.boxCounter=0
    """)

    ui.on('boxCreated',createBox )
    ui.on('boxModified', boxModifiedHandelr)

    with ui.header().style('background-color: #3874c8').classes('items-center justify-between bg-stone-900').style(""" background-color: var(--color-stone-900);"""):
        ui.button(on_click=lambda: left_drawer.toggle(), icon='s_grid_view').props('flat color=white')
        ui.button('Export').props('flat color=amber')
        ui.label('LabelIt!')
        modifyClassesModal()
        ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
        
    with ui.left_drawer(top_corner=True, bottom_corner=True, fixed=False).classes('bg-stone-800').classes('px-2 items-center') as left_drawer:
        imagesDrawer()   
         
    with ui.right_drawer(top_corner=True, bottom_corner=True, fixed=False).classes('bg-stone-800').classes('') as right_drawer:
        labelsDrawer()    
             
    with ui.row().classes('w-full h-full justify-center items-center').classes('p-4'):
        ui.html("""
                <canvas
                    id="myCanvas"
                    style=" display: block; border: 1px solid black"
                ></canvas>
            """, sanitize=False)           

        cerateCanvas()
        


        


           