from flask import Flask, request, jsonify
from langchain_community.llms import Ollama
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

# llm = Ollama(model='llama3')
#
# response = llm.invoke('Tell me a cat joke?')
# print(response)

UPLOAD_FOLDER = os.path.expanduser('~') + '/pdf'

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


def save_files(files):
    saved_files = []
    if files:
        for file in files:
            saved_files.append(file.name)
            full_filename = UPLOAD_FOLDER + '/' + file.filename
            file.save(full_filename)
            saved_files.append(full_filename)
    return saved_files


def get_pdf_file_contents(files):
    text = ''
    for file in files:
        if file == 'files':
            pass
        else:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    return text


def get_text_chunks(content):
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(content)


@app.route('/api/v1/files/upload', methods=['POST'])
def process_upload_files():
    if 'files' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    files = request.files.getlist('files') or False
    # save files
    saved_files = save_files(files)
    # read files
    raw_text = get_pdf_file_contents(saved_files)
    # get text chunks
    text_chunks = get_text_chunks(raw_text)
    #create vector store


    response = {
        'status': 'success',
        'code': 200,
        'saved_files': saved_files,
        'raw_text': raw_text,
        'chunks': text_chunks
    }
    return response, 201


def start_app():
    app.run(host='192.168.1.81', port=3000, debug=True)


if __name__ == '__main__':
    start_app()
