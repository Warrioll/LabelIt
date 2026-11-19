from nicegui import ui
from utils import basicAppSettings
from pages.workspace.layout.objectDetectionDrawer import objectDetectionDrawer
from pages.workspace.layout.imagesDrawer import imagesDrawer
import state
from pages.workspace.editClassesModal.editClassesModal import editClassesModal
from pages.workspace.layout.imageRecognitionDrawer import imageRecognitionDrawer
import utils
from pages.workspace.layout.footer import footer
import pages.workspace.canvas as canvas
from pages.workspace.exitModal import exitModal

def workspacePage():
    print('Worksapce')
    basicAppSettings('Worksapce')
    if len(state.files)==0:
        ui.navigate.to('/')
        return 

    # tu był oui. add-head html

    # tu były create fabric canvas, handlery i create eventy
    #     #nonlocal boxCounter
    #     exampleClass=state.classesList.getExampleClass()
    #     state.currentImg.appendBox(Box(state.boxCounter, (e.args["left"], e.args["top"]), e.args["width"],e.args["height"], exampleClass))
    #     #print('new Box:',(e.args["left"], e.args["top"]), e.args["width"],e.args["height"])
    #     utils.drawBox(state.boxCounter,e.args["left"],e.args["top"],e.args["width"],e.args["height"], exampleClass.color['value'])


    #     state.boxCounter+=1#int(e.args["boxId"])+1
    #     #boxCounter+=1

    state.currentImg=state.files[0]
    state.refreshFooter=footer.refresh

    # tu było ustanianie w js poczatkowego maxHeight i maxwidth i scale p

    # Tu były ui.on

    canvas.setCanvasEventsHandlers()

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

    with ui.header().classes('items-center justify-between bg-stone-900').style(""" background-color: var(--color-stone-900);"""):
        ui.button(on_click=lambda: left_drawer.toggle(), icon='s_grid_view').props('flat color=amber')
        with ui.element('div').classes('flex justify-center flex-grow items-center '):
            
        #ui.label('LabelIt!')
            ui.html("""
                <strong class="text-lg mb-0 mx-5">
                                Label<span class="text-yellow-500  mb-0">It</span>!
                </strong>
            """)
            with ui.button('Image').props('flat color=amber no-caps'):

                            def copyLabelsHandler(imgId:int):
                                 if imgId<0:
                                      ui.notify('There is no previous image', classes='bg-white text-black')
                                 elif imgId>=len(state.files):
                                      ui.notify('There is no next image', classes='bg-white text-black')
                                 else:
                                    state.currentImg.appendMultipleBoxes(state.files[imgId].getBoxesListCopy())
                                    state.refreshBoxesList()
                                    canvas.refreshCanvas() 

                            def deleteBoxesHandler():
                                 canvas.eraseAllBoxes()
                                 state.currentImg.boxes.clear()
                                 state.refreshBoxesList()
                             
                            with ui.menu().props('dark').classes('shadow-none bg-stone-800 border-1 border-stone-700' ):
                                ui.menu_item(' Delete all labels from image',on_click=deleteBoxesHandler)
                                ui.separator()
                                with ui.menu_item('Copy labels from ', auto_close=False):
                                    with ui.item_section().props('side'):
                                        ui.icon('keyboard_arrow_right')

                                    with ui.menu().props('dark anchor="top end" self="top start" auto-close' ).classes(' ml-1 shadow-none bg-stone-800 border-1 border-stone-700'):
                                    
                                        items_count = len(state.files)
                                        item_height = 48
                                        max_height = 500
                                        scroll_height = min(items_count * item_height, max_height)

                                        with ui.scroll_area().classes('min-w-100').style(  f'height: {scroll_height}px;'  ).props('dark'):
                                            ui.menu_item('Previous image', on_click=lambda e: copyLabelsHandler(state.files.index(state.currentImg)-1)).classes('w-full')
                                            ui.separator()
                                            ui.menu_item('Next image', on_click=lambda e: copyLabelsHandler(state.files.index(state.currentImg)+1)).classes('w-full')
                                            ui.separator().props('dark')
                                            for i in range(items_count):
                                                ui.menu_item(state.files[i].name, on_click=lambda idx=i: copyLabelsHandler(idx)).classes('w-full')
                                                ui.separator()
                                
            editClassesModal()
            with ui.button('Export').props('flat color=amber no-caps'):
                with ui.menu().props('dark').classes('shadow-none bg-stone-800 border-1 border-stone-700') as menu:
                    ui.menu_item('Export object detection files (YOLO format)', on_click=lambda: ui.download(utils.createObjectDecectionZip(state.files), f'LabelIt_Object_Detection_YOLO_{utils.getCurrentDateStringForFileName()}.zip'))
                    ui.separator()
                    #ui.menu_item('Export image recognition JSON file',  on_click=lambda: ui.download(utils.createImageRecognitionJSONFile(state.files), f'LabelIt_Image_Recognition_{utils.getCurrentDateStringForFileName()}.json'))
                    ui.menu_item('Export image recognition CSV file',on_click=lambda: ui.download(utils.createImageRecognitionCSVFile(state.files, state.imagesClassesList.classes), f'LabelIt_Image_Recognition_{utils.getCurrentDateStringForFileName()}.csv'))
            exitModal()
        ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=amber')

    with ui.footer().classes('items-center justify-between text-center bg-stone-900').style(""" background-color: var(--color-stone-900);"""):
        footer()



                   
                        
             
    with ui.element('div').classes(
        'absolute inset-0 flex justify-center items-center overflow-auto p-4'
    ).style('top: 20px; bottom: 0;').props('id=canvasContainer'):
        canvas.createHTMLCanvas()
        canvas.cerateFabricCanvas()
        state.setImgAsCurrentImg(state.files[0], canvas.refreshCanvas)
        


        


           