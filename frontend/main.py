import streamlit as st
from streamlit_option_menu import option_menu

import upload, home, chat, contact

st.set_page_config(
    page_title="SCIAM RAG"
)


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append(
            {
                'title': title,
                'function': function
            }
        )

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='SCIAM RAG',
                options=['Home', 'Chat', 'Importer', 'Contact'],
                icons=['house', 'chat-dots', 'file-arrow-down', 'envelope-dash'],
                menu_icon='cpu',
                default_index=0,
                styles={
                    'container': {
                        'padding': '5 !important',
                        'background-color': 'white',
                    },
                    'icon': {
                        'color': 'black',
                        'font-size': '23px'
                    },
                    'nav-link': {
                        'color': 'black',
                        'font-size': '20px',
                        'text-align': 'left',
                        '--hover-color': '#9494CF',
                        'margin': '0px'

                    },
                    'nav-link-selected': {
                        'color': 'white',
                        'background-color': '#7676C4'
                    }
                }
            )
        if app == 'Home':
            home.app()
        if app == 'Chat':
            chat.app()
        if app == 'Importer':
            upload.app()
        if app == 'Contact':
            contact.app()

MultiApp().run()
