from nicegui import ui
import state
import utils
import pages.workspace.canvas as canvas

@ui.refreshable
def footer():

    def changeStatusHandler(value):
        state.currentImg.updateStatus(value)
        progressBar.refresh()

    def nextImgHandler():
        idx=utils.findCurrentImgIndex(state.files, state.currentImg)
        changeStatusHandler('Done')
        if idx+1>=len(state.files):
              ui.notify('There is no next image', classes='bg-white text-black')            
        else:
            
            state.setImgAsCurrentImg(state.files[idx+1], canvas.refreshCanvas)

    def prevImgHandler():
        idx=utils.findCurrentImgIndex(state.files, state.currentImg)
        if idx-1<0:
              ui.notify('There is no previous image', classes='bg-white text-black')            
        else:
            state.setImgAsCurrentImg(state.files[idx-1], canvas.refreshCanvas)

    

    @ui.refreshable
    def progressBar():
        counter=0
        review=0
        amountOfImgs=len(state.files)
        for file in state.files:
            if file.status=='Done': counter+=1
            elif file.status=='Review': review+=1
        ui.linear_progress(value=counter/amountOfImgs, show_value=False).classes('w-40 ml-5 bg-stone-700').props(' rounded dense color=white ') 
        ui.label(str(counter)+'/'+str( amountOfImgs)+' ('+str(int(counter/amountOfImgs*100))+'%) | '+str(review)+' in review').classes('ml-3 text-stone-400')

    with ui.row().classes('w-full items-center no-wrap justify-between pb-2'):
        with ui.row().classes('w-full items-center no-wrap justify-start'):
            progressBar()
        with ui.row().classes('w-full items-center no-wrap justify-center'):
            with ui.button(icon='arrow_back_ios', on_click=prevImgHandler).props('dense, flat color=amber size=xs').classes('w-3'):
                ui.tooltip('Previous image').classes('text-xs bg-stone-800 text-center')
            ui.label(state.currentImg.name).classes('text-stone-400 mx-2')
            with ui.button(icon='arrow_forward_ios', on_click=nextImgHandler).props('dense, flat color=amber size=xs').classes('w-3'):
                ui.tooltip('Next image').classes('text-xs bg-stone-800 text-center')
        with ui.row().classes('w-full items-center no-wrap justify-end'):        
            radio1 = ui.radio(['Todo', 'Review', 'Done'], value=state.currentImg.status, on_change=lambda e: changeStatusHandler(e.value)).props(' dark inline dense color=amber size=xs').classes('mr-5  text-stone-400')