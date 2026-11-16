from nicegui import ui, events
import utils
import state 
from classes.Box import Box

def cerateFabricCanvas():
        ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/fabric@5/dist/fabric.min.js"></script>')
        
        imgW, imgH = state.currentImg.getImageSize()

        ui.run_javascript("""

            const container = document.getElementById('canvasContainer');

            window.maxCanvasHeight= container.clientHeight- 36;
            window.maxCanvasWidth= container.clientWidth- 32;   
            window.canvasScale=Math.min(window.maxCanvasHeight/"""+str(imgH)+""", window.maxCanvasWidth/"""+str(imgW)+""")




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
        
        if (!(Math.floor(width)===0 && Math.floor(height)===0)){  
            
            emitEvent('boxCreated', {
                   
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
    box = next((b for b in state.currentImg.boxes if b.boxId == e.args["boxId"]), None)
    if not(box is None):
        box.position=(float(e.args["left"]), float(e.args["top"]))
        box.width=float(e.args["width"])
        box.height=float(e.args["height"])

def boxDeselectedHandler(e):
    state.selectedLabelBoxId= None
    state.refreshBoxesList()

def createBox(e):
    #nonlocal boxCounter
    exampleClass=state.classesList.getExampleClass()
    newBox=Box( (e.args["left"], e.args["top"]), e.args["width"],e.args["height"], exampleClass)
    state.currentImg.appendBox(newBox)
    #print('new Box:',(e.args["left"], e.args["top"]), e.args["width"],e.args["height"])
    drawBox(newBox.boxId,e.args["left"],e.args["top"],e.args["width"],e.args["height"], exampleClass.color['value'])
    #boxCounter+=1

def createHTMLCanvas():
    ui.html("""
                <canvas
                    id="myCanvas"
                    style="display: block; border: 1px solid black"
                ></canvas>
            """, sanitize=False)
    
def setCanvasEventsHandlers():
    ui.on('boxCreated',createBox )
    ui.on('boxModified', boxModifiedHandelr)
    ui.on('boxDeselected', boxDeselectedHandler)

def drawBox(boxId: str, left: float, top:float, width:float, height:float, color: str):
      
      ui.run_javascript("""
                        const color ='"""+color+"""'
                        const fillColor = new fabric.Color( color).setAlpha(0.3).toRgba();

                        const croppedImg=  new fabric.Rect({
                                         id: '"""+boxId+"""',
                                         left: """+str(left)+"""*window.canvasScale,
                                         top: """+str(top)+"""*window.canvasScale,
                                         width: """+str(width)+"""*window.canvasScale,
                                         height: """+str(height)+"""*window.canvasScale, 
                                         fill: fillColor,//'rgba(230, 198, 91, 0.3)',
                                         stroke: color,//'rgba(219, 166, 84, 1)',
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

def drawAllCurrrentImgBoxes():
    box:Box
    for box in state.currentImg.boxes:
        drawBox(box.boxId,box.position[0],box.position[1],box.width,box.height, box.labelClass.color['value'])

def setNewCanvasImgAndScale():
    imgW, imgH =state.currentImg.getImageSize()

    ui.run_javascript("""
                    window.canvasScale=Math.min(window.maxCanvasHeight/"""+str(imgH)+""", window.maxCanvasWidth/"""+str(imgW)+""")
                
                    window.myCanvas.getObjects('rect').forEach(rect => {
                        window.myCanvas.remove(rect);
                    });
    
                    window.setCanvasImg('"""+state.currentImg.getUrl()+"""', window.canvasScale, """+str(imgW)+""", """+str(imgH)+""")
                """)

def eraseAllBoxes():
    ui.run_javascript("""
                    window.myCanvas.getObjects('rect').forEach(rect => {
                        window.myCanvas.remove(rect);
                    });
                """)

def eraseBox(boxId:str):
    ui.run_javascript("""
                const rect = window.myCanvas.getObjects().find(obj => obj.id === '"""+str(boxId)+"""');
    
                if (rect) {
                    window.myCanvas.remove(rect);
                    window.myCanvas.requestRenderAll();
                }
            """)
def markBox(boxId:str):
    ui.run_javascript("""
                const rect = window.myCanvas.getObjects().find(obj => obj.id === '"""+boxId+"""');
    
                if (rect) {
                    window.myCanvas.setActiveObject(rect);
                    window.myCanvas.requestRenderAll(); 
                }
            """)

def refreshCanvas():
    eraseAllBoxes()
    setNewCanvasImgAndScale()
    drawAllCurrrentImgBoxes()