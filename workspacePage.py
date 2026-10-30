from nicegui import ui, events
from utils import basicAppSettings
from PIL import Image

def workspacePage(files:list):
    print('Worksapce')
    basicAppSettings('Worksapce')
    # if len(files)==0:
    #     ui.navigate.to('/')
    imgs=['C:\\Users\\lorak\\Desktop\\magisterka\\datasets\\Farma 2\\DJI_20230921113850_0001_T.JPG', 'C:\\Users\\lorak\\Desktop\\magisterka\\datasets\\Farma 2\\DJI_20230921113853_0005_T.JPG', 'C:\\Users\\lorak\\Desktop\\magisterka\\datasets\\Farma 2\\DJI_20230921113854_0006_T.JPG']
    #pilImages= [ Image(file.read()) for file in files]
    print('pil imgs: ', len(files))
    #print(type(files[0]))

    with ui.header().style('background-color: #3874c8').classes('items-center justify-between bg-stone-900').style("""

    background-color: var(--color-stone-900);
"""):
        ui.button(on_click=lambda: left_drawer.toggle(), icon='s_grid_view').props('flat color=white')
        ui.label('LabelIt!')
        ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
        
    with ui.left_drawer(top_corner=True, bottom_corner=True, fixed=False).classes('bg-stone-800').classes('px-2 items-center') as left_drawer:
      ui.label('IMAGES').classes(' py-3 w-full justify-center text-center')
      with ui.grid(columns=2):
        # for img in files:
        #     ui.image(img).classes('w-28')
        for img in imgs:
            with ui.button():
                ui.image(Image.open(img)).classes('w-32 m-1')

    with ui.right_drawer(top_corner=True, bottom_corner=True, fixed=False).classes('bg-stone-800').classes('') as right_drawer:
          ui.label('LABELS').classes('px-6 py-3 w-full justify-center text-center')

    with ui.row().classes('w-full h-full justify-center items-center').classes('p-4'):
        # startPos: list[float,float] | None = [None, None]
        # endPos: list[float,float] | None = [None, None]
        # drag=False
        # def mouse_handler(e: events.MouseEventArguments):
        #     nonlocal startPos, endPos, drag
        #     if e.type == 'mousedown': 
        #             startPos[0]=e.image_x
        #             startPos[1]=e.image_y
        #             endPos[0]=e.image_x
        #             endPos[1]=e.image_y
        #             drag=True
        #             ui.notify(f'start')
        #     elif e.type == 'mousemove': 
        #         endPos[0]=e.image_x
        #         endPos[1]=e.image_y 
        #     elif e.type == 'mouseup' :
        #         print('start: ', startPos)
        #         print('end: ', endPos)    
        #         startPos = [None, None]
        #         endPos=  [None, None]
        #         drag=False
        #         ui.notify(f'drop')
                
        #     color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'
        #     if drag:
        #         endPos[0]=e.image_x
        #         endPos[1]=e.image_y
        #         ii.content += f'<rect id="A" x="{startPos[0]:.1f}" y="{startPos[1]:.1f}" width="{abs(endPos[0]-startPos[0])}" height="{abs(endPos[1]-startPos[1])}" fill="green" stroke="blue" cursor="pointer" />'
        #         ii.update() 
        #     print('>m: ', e.type, flush=True)

        # src = 'C:\\Users\\lorak\\Desktop\\magisterka\\datasets\\Farma 2\\DJI_20230921113850_0001_T.JPG'
        # ii = ui.interactive_image(src, on_mouse=mouse_handler, events=[ 'mousedown', 'mouseup', 'mousemove'], cross=True, sanitize=False)

        # l1= ii.addLayer()
        # print('l1: ', dir(l1), flush=True)

        #//////////////////////////////////////
        # ui.add_head_html(
        #     '<script src="https://cdn.jsdelivr.net/npm/'
        #     'fabric@5.3.1/dist/fabric.min.js"></script>'
        # )
        ui.add_head_html("""
        <script src="https://cdn.jsdelivr.net/npm/fabric@5/dist/fabric.min.js"></script>
\
        """)

        #with ui.card().classes('w-[80%]'):
        ui.html("""
                <canvas
                    id="yolo_canvas"
                    width="900"
                    height="600"
                    style="border: 2px solid black; display: block;"
                ></canvas>
            """, sanitize=False)

        def cerateCanvas():
               result= ui.run_javascript("""
                    const el = document.getElementById('yolo_canvas');

                         if (!el) {
                             return 'Nie znaleziono canvasu';
                         }
                         if (el.dataset.fabricInitialized === 'true') return;

                         if (typeof window.fabric === 'undefined') {
                             return 'Fabric.js nie jest załadowany';
                         }

                            
                const canv =  new window.fabric.Canvas(el, {
                                            //backgroundImage: ,
                                            selection: true
                                        });
                   fabric.Image.fromURL('"""+imgs[0]+"""', function(img) {
                        canv.setBackgroundImage(img, canv.renderAll.bind(canv));
});

                """)
               #ui.notify(result)
        cerateCanvas()

            # ui.run_javascript("""
            #         (() => {
            #             const el = document.getElementById('yolo_canvas');

            #             if (!el) {
            #                 return 'Nie znaleziono canvasu';
            #             }

            #             if (typeof window.fabric === 'undefined') {
            #                 return 'Fabric.js nie jest załadowany';
            #             }

            #             if (window.yoloCanvas) {
            #                 window.yoloCanvas.dispose();
            #                 window.yoloCanvas = null;
            #             }

            #             window.yoloCanvas = new window.fabric.Canvas(el, {
            #                 backgroundColor: 'red',
            #                 selection: true
            #             });

            #             window.yoloCanvas.add(new window.fabric.Rect({
            #                 left: 100,
            #                 top: 100,
            #                 width: 150,
            #                 height: 100,
            #                 fill: 'rgba(0, 255, 0, 0.3)',
            #                 stroke: 'green',
            #                 strokeWidth: 3
            #             }));

            #             window.yoloCanvas.renderAll();

            #             return 'OK — canvas utworzony';
            #         })()
            #     """)

            #     ui.notify(str(result))

            # ui.button('Uruchom canvas', on_click=init_canvas)





       
#         ui.interactive_image('C:\\Users\\lorak\\Desktop\\magisterka\\datasets\\Farma 2\\DJI_20230921113850_0001_T.JPG', cross='green', content='''
#     <rect id="A" x="85" y="70" width="80" height="60" fill="none" stroke="red" pointer-events="all" cursor="pointer" />
#     <rect id="B" x="180" y="70" width="80" height="60" fill="none" stroke="red" pointer-events="all" cursor="pointer" />
# ''', sanitize=False).on('svg:pointerdown', lambda e: ui.notify(f'SVG clicked: {e.args}')).classes('w-full h-full')