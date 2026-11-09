from nicegui import ui
import state

@ui.refreshable
def footer():
    ui.label(state.currentImg.name).classes('ml-3 text-stone-400')