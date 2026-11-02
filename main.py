from nicegui import ui
from homePage import homePage
from workspacePage import workspacePage

APP_URL='http://127.0.0.1:8080/'

# def basicAppSettings(pageSubtitle: str=''):
#         ui.page_title('LabelIt! - '+pageSubtitle)
#         ui.add_head_html('''
# <style>
# :root{
# --nicegui-default-padding: 0rem;
# --nicegui-default-gap: 0rem;

# color: white;
# background-color: oklch(21.6% 0.006 56.043);
# }

# </style>
# ''')


files=[]

@ui.page('/')
def home():
     homePage(files)

@ui.page('/workspace')
def worksapce():
       workspacePage()


ui.run()
                