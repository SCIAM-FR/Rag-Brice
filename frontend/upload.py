import streamlit as st
import requests
from PyPDF2 import PdfReader




def get_raw_text(files):
    text = ''
    for file in files:
        file_read = PdfReader(file)
        for page in file_read.pages:
            text += page.extract_text()
    return text


def app():
    st.title('Importer des fichiers')

    uploaded_files = st.file_uploader("Charger vos doucments PDF et cliquer sur 'Traiter'", accept_multiple_files=True)
    if st.button('Traiter'):
        with st.spinner('En cours...'):
            if uploaded_files:
                files = [('files', (uploaded_file.name, uploaded_file, uploaded_file.type)) for uploaded_file in
                         uploaded_files]

                # call the backend with the file
                response = requests.post('http://192.168.1.81:3000/api/v1/files/upload', files=files)
                st.write(response.json())
