from nicegui import ui, events
from utils import basicAppSettings
from PIL import Image
from DatasetImage import DatasetImage
from pathlib import Path
from Box import Box
from objectDetectionDrawer import objectDetectionDrawer
from imagesDrawer import imagesDrawer
import state
from editClassesModal.editClassesModal import editClassesModal
from imageRecognitionDrawer import imageRecognitionDrawer
import utils
from footer import footer

def workspacePage():
    print('Worksapce')
    basicAppSettings('Worksapce')
    if len(state.files)==0:
        ui.navigate.to('/')
        return 

    ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/fabric@5/dist/fabric.min.js"></script>')

    

    def cerateCanvas():
        imgW, imgH = state.currentImg.getImageSize()

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

            el.width="""+str(imgW)+"""*window.canvasScale
            el.height="""+str(imgH)+"""*window.canvasScale

            window.myCanvas=  new window.fabric.Canvas(el, {
                selection: false,     
                skipTargetFind: false,
                
                });
            el.dataset.fabricInitialized = 'true';

            /* window.setCanvasImg=(imgUrl, scale)=>{
                fabric.Image.fromURL(imgUrl, function(img) {
                    window.myCanvas.setBackgroundImage(img, window.myCanvas.renderAll.bind(window.myCanvas), {
                        scaleX: scale,
                        scaleY: scale,
                        });
                    });
                }
                */

            window.setCanvasImg = (imgUrl, scale, imgW, imgH) => {
                // Zmiana rozmiaru canvasa
                window.myCanvas.setDimensions({
                    width: imgW * scale,
                    height: imgH * scale
                });

                // Załadowanie nowego zdjęcia
                fabric.Image.fromURL(imgUrl, function(img) {
                    window.myCanvas.setBackgroundImage(
                        img,
                        window.myCanvas.renderAll.bind(window.myCanvas),
                        {
                            scaleX: scale,
                            scaleY: scale
                        }
                    );
                });
            };
                
            window.rectPreview=null
            window.setCanvasImg('"""+state.currentImg.getUrl()+"""',window.canvasScale, """+str(imgW)+""", """+str(imgH)+""")
         """)

        createMouseDownEvent()
        createMouseUpEvent()
        createMouseMoveEvent()
        createModifiedBoxEvent()
        createDeselectedBoxEvent()

    def createMouseDownEvent():
        ui.run_javascript("""
        window.myCanvas.on('mouse:down', function(opt) {
                    window.isDrawingRect = !opt.target;
                    if ( window.isDrawingRect) {
                        const pointer = window.myCanvas.getPointer(opt.e);

                        window.rectPreview= new fabric.Rect({
                            left:  pointer.x,
                            top:  pointer.y,
                            width: 1,
                            height: 1,
                            fill: 'rgba(250, 250, 250, 0.2)',//'rgba(230, 198, 91, 0.2)',
                            stroke: 'white',
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
           if (window.isDrawingRect && window.rectPreview) {
                window.myCanvas.remove(window.rectPreview);
                const pointer = window.myCanvas.getPointer(opt.e);
                window.rectPreview=null

            const left =      Math.min(window.startRect.x, pointer.x)
            const top =    Math.min(window.startRect.y, pointer.y)
            const width = Math.abs(window.startRect.x - pointer.x)
            const height = Math.abs(window.startRect.y - pointer.y)
            //const boxId="""+str(state.boxCounter)+"""//window.boxCounter
            //window.boxCounter++

            if (!(Math.floor(width)===0 && Math.floor(height)===0)){  

                
                emitEvent('boxCreated', {
                        //boxId: """+str(state.boxCounter)+""",
                        left:  left/window.canvasScale,
                        top: top/window.canvasScale,
                        width: width/window.canvasScale,
                        height: height/window.canvasScale,
                    });
            }
            }
            
        });


        

        """)
        #state.boxCounter+=1

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

    def createDeselectedBoxEvent():
        ui.run_javascript("""
            window.myCanvas.on('selection:cleared', function(opt) {
                //const deselectedBoxes = opt.deselected || [];

              emitEvent('boxDeselected')
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

    def boxDeselectedHandler(e):
        state.selectedLabelBoxId= None
        state.refreshBoxesList()
 
    def createBox(e):
        #nonlocal boxCounter
        exampleClass=state.classesList.getExampleClass()
        state.currentImg.appendBox(Box(state.boxCounter, (e.args["left"], e.args["top"]), e.args["width"],e.args["height"], exampleClass))
        #print('new Box:',(e.args["left"], e.args["top"]), e.args["width"],e.args["height"])
        utils.drawBox(state.boxCounter,e.args["left"],e.args["top"],e.args["width"],e.args["height"], exampleClass.color['value'])
        
        # ui.run_javascript("""
        #     const box=  new fabric.Rect({
        #                    id: """+str(state.boxCounter)+""",
        #                    left:  """+str(e.args["left"])+"""*window.canvasScale,
        #                     top: """+str(e.args["top"])+"""*window.canvasScale,
        #                     width: """+str(e.args["width"])+"""*window.canvasScale,
        #                     height: """+str(e.args["height"])+"""*window.canvasScale,
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
        #               box.setControlsVisibility({
        #                    mtr: false
        #                }); 
        #                window.myCanvas.add(box);
        #                window.myCanvas.renderAll();

        # """)

        state.boxCounter+=1#int(e.args["boxId"])+1
        #boxCounter+=1


    state.currentImg=state.files[0]
    # for img in state.files:
    #     img.boxes.clear()
    state.refreshFooter=footer.refresh
    imgW, imgH = state.currentImg.getImageSize()

    ui.run_javascript("""

    /*
        window.addEventListener('beforeunload', function (e) {
            e.preventDefault();
            e.returnValue = '';
        });
        */

        const container = document.getElementById('canvasContainer');

        window.maxCanvasHeight= container.clientHeight- 36;
        window.maxCanvasWidth= container.clientWidth- 32;   
        window.canvasScale=Math.min(window.maxCanvasHeight/"""+str(imgH)+""", window.maxCanvasWidth/"""+str(imgW)+""")
        //window.boxCounter=0
    """)

    ui.on('boxCreated',createBox )
    ui.on('boxModified', boxModifiedHandelr)
    ui.on('boxDeselected', boxDeselectedHandler)

    with ui.header().classes('items-center justify-between bg-stone-900').style(""" background-color: var(--color-stone-900);"""):
        ui.button(on_click=lambda: left_drawer.toggle(), icon='s_grid_view').props('flat color=amber')
        with ui.element('div').classes('flex justify-center flex-grow items-center '):
            
        #ui.label('LabelIt!')
            ui.html("""
                <strong class="text-lg mb-0 mx-5">
                                Label<span class="text-yellow-500  mb-0">It</span>!
                </strong>
            """)
            editClassesModal()
            with ui.button('Export').props('flat color=amber no-caps'):
                with ui.menu().props('dark').classes('shadow-none bg-stone-800 border-1 border-stone-700') as menu:
                    ui.menu_item('Export object detection files (YOLO format)', on_click=lambda: ui.download(utils.createObjectDecectionZip(state.files), f'LabelIt_Object_Detection_YOLO_{utils.getCurrentDateStringForFileName()}.zip'))
                    ui.separator()
                    #ui.menu_item('Export image recognition JSON file',  on_click=lambda: ui.download(utils.createImageRecognitionJSONFile(state.files), f'LabelIt_Image_Recognition_{utils.getCurrentDateStringForFileName()}.json'))
                    ui.menu_item('Export image recognition CSV file',on_click=lambda: ui.download(utils.createImageRecognitionCSVFile(state.files, state.imagesClassesList.classes), f'LabelIt_Image_Recognition_{utils.getCurrentDateStringForFileName()}.csv'))
            
        ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=amber')

    with ui.footer().classes('items-center justify-between text-center bg-stone-900').style(""" background-color: var(--color-stone-900);"""):
        footer()


    with ui.left_drawer(top_corner=True, bottom_corner=True, fixed=False).classes('bg-stone-800').classes('px-2 items-center') as left_drawer:
        imagesDrawer()   
         
    with ui.right_drawer(top_corner=True, bottom_corner=True, fixed=False).classes('bg-stone-800').classes('') as right_drawer: 
            with ui.tabs().classes('w-full').props('dense color=amber indicator-color=amber active-color=amber') as tabs:
                one = ui.tab('Detection').classes('whitespace-normal').props('color=amber no-caps')
                two = ui.tab('Recognition').classes('whitespace-normal').props('color=amber no-caps')
            with ui.tab_panels(tabs, value=one).classes('w-full h-full bg-stone-800').props('dark'):
                with ui.tab_panel(one):
                    objectDetectionDrawer()
                with ui.tab_panel(two):
                    imageRecognitionDrawer()
                   
                        
             
    # with ui.row().classes('w-full h-full justify-center items-center').classes('p-4'):
    #     with ui.element('div').classes(
    #         'w-full h-full flex justify-center items-center overflow-auto p-4'
    #     ):
    #         ui.html("""
    #             <canvas
    #                 id="myCanvas"
    #                 style="display: block; border: 1px solid black"
    #             ></canvas>
    #         """, sanitize=False)
          

    #         cerateCanvas()
    with ui.element('div').classes(
        'absolute inset-0 flex justify-center items-center overflow-auto p-4'
    ).style('top: 20px; bottom: 0;').props('id=canvasContainer'):
        ui.html("""
            <canvas
                id="myCanvas"
                style="display: block; border: 1px solid black"
            ></canvas>
        """, sanitize=False)

        cerateCanvas()
        


        


           