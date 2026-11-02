from nicegui import ui

def basicAppSettings(pageSubtitle: str=''):
        ui.page_title('LabelIt! - '+pageSubtitle)
        ui.add_head_html('''
<style>
:root{
--nicegui-default-padding: 0rem;
--nicegui-default-gap: 0rem;

color: white;
background-color: oklch(21.6% 0.006 56.043);
}

</style>
''')

