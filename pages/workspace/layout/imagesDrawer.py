from nicegui import ui, events
from classes.Box import Box
from classes.DatasetImage import DatasetImage
from typeguard import typechecked
import state
from nicegui.events import GenericEventArguments
import pages.workspace.canvas as canvas

@typechecked
def imagesDrawer():

    markup='bg-amber-400 text-stone-900'
    #selectedImgButton:ui.button|None=None
    def setCanvasImg(e: GenericEventArguments,img: DatasetImage):
            #nonlocal selectedImgButton
            state.currentImg=img
            state.refreshFooter()
            imgW, imgH = state.currentImg.getImageSize()

            canvas.eraseAllBoxes()
            canvas.setNewCanvasImgAndScale(imgW, imgH)

            canvas.drawAllCurrrentImgBoxes()

            # if not (selectedImgButton is None):
            #     selectedImgButton.classes(remove=markup)
            #     elements = selectedImgButton.descendants()
            #     label = next((el for el in elements  if isinstance(el, ui.label)), None)
            #     label.classes(remove='text-stone-900')
            #     label.classes(add='text-amber-400')
            # selectedImgButton=e.sender
            # selectedImgButton.classes(markup)
            # elements = selectedImgButton.descendants()
            # label = next((el for el in elements  if isinstance(el, ui.label)), None)
            # label.classes(add='text-stone-900')
            state.refreshBoxesList()
            state.refreshClassesList()

    @ui.refreshable
    def imagesButtons():
         for i in range(len(state.files)):
                             with ui.button(on_click=lambda im=state.files[i]: state.setImgAsCurrentImg(im, canvas.refreshCanvas)).props('flat dense color=amber').classes('p-0 m-1') as btn:
                                             
         
                                 
                                 ui.image(state.files[i].getThumbnail()).classes(
                                        'w-32 h-20 m-1 object-contain border-1 border-stone-900'
                                    )
                                 label = ui.label(state.files[i].name).classes('w-full break-all no-caps text-left mx-2 mb-1 text-xs text-amber-400')
                                 state.files[i].buttonLabel=label
                                 state.files[i].button=btn


                                #  if state.currentImg is state.files[i]:
                                #        btn.classes(markup)
                                #        label.classes(add='text-stone-900')
         
                                #  if i==0:
                                #      btn.classes(markup)
                                #      #selectedImgButton=btn 
                                #      label.classes(add='text-stone-900')        
         
                                 # @ui.refreshable
                                 # def label(btn=btn):
                                 #     if btn==selectedImgButton:
                                 #         ui.label(state.files[i].name).classes('w-full break-all no-caps text-left mx-2 mb-2 text-xs text-stone-900')
                                 #     else:
                                 #         ui.label(state.files[i].name).classes('w-full break-all no-caps text-left mx-2 mb-2 text-xs text-amber-400')
                                 # label()
         
                                 @ui.refreshable
                                 def badge(index=i):
                                         bd= ui.badge(state.files[index].status).props('floating dense ').classes(' border-1 border-stone-800')
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

    state.refreshImagesList=imagesButtons.refresh

    ui.label('IMAGES').classes(' py-3 w-full justify-center text-center')
    with ui.scroll_area().props('dark').classes('h-full'):
        with ui.button_group().props('unelevated'):
            with ui.grid(columns=2):
                  imagesButtons()
                
    