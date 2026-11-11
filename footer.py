from nicegui import ui
import state
import utils

@ui.refreshable
def footer():

    def changeStatusHandler(e):
        state.currentImg.updateStatus(e.value)
        progressBar.refresh()

    def nextImgHandler(e):
        idx=utils.findCurrentImgIndex(state.files, state.currentImg)
        #TODO

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

    with ui.row().classes('w-full items-center no-wrap justify-between pb-1'):
        with ui.row().classes('w-full items-center no-wrap justify-start'):
            progressBar()
        with ui.row().classes('w-full items-center no-wrap justify-center'):
            ui.button(icon='arrow_back_ios').props('dense, flat color=amber size=xs')
            ui.label(state.currentImg.name).classes('text-stone-400')
            ui.button(icon='arrow_forward_ios').props('dense, flat color=amber size=xs')
        with ui.row().classes('w-full items-center no-wrap justify-end'):        
            radio1 = ui.radio(['Todo', 'Review', 'Done'], value=state.currentImg.status, on_change=changeStatusHandler).props(' dark inline dense color=amber size=xs').classes('mr-5  text-stone-400')