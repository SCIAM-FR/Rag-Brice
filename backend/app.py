from flask import Flask, request, jsonify
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains.question_answering import load_qa_chain
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

llm = Ollama(model='llama3')

embeddings = FastEmbedEmbeddings()

UPLOAD_FOLDER = os.path.expanduser('~') + '/RAG/pdf'
DB_FOLDER = os.path.expanduser('~') + '/RAG/db_store'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)


def save_files(files):
    saved_files = []
    if files:
        for file in files:
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
        return jsonify({'success': False, 'code': 400, 'message': 'No file part'}), 400
    files = request.files.getlist('files') or False
    # save files
    saved_files = save_files(files)
    # read files
    raw_text = get_pdf_file_contents(saved_files)
    # get text chunks
    chunks = get_text_chunks(raw_text)
    # create vector store
    vector_store = Chroma.from_texts(texts=chunks, embedding=embeddings, persist_directory=DB_FOLDER)

    vector_store.persist()

    response = {
        'status': True,
        'code': 200,
        'saved_files': saved_files,
        'raw_text': raw_text,
        'chunks': chunks
    }
    return response, 201


@app.route('/api/v1/questions', methods=['POST'])
def process_questions():
    json_question = request.json
    if 'content' not in json_question or len(json_question) == 0:
        return {
            'status': False,
            'code': 400,
            'message': 'Content of question is required'
        }

    vector_store = Chroma(persist_directory=DB_FOLDER, embedding_function=embeddings)

    retriever = vector_store.similarity_search(json_question.get('content'))

    chain = load_qa_chain(llm=llm, chain_type='stuff')

    response = chain({'input_documents': retriever, 'question': json_question.get('content')})
    if response:
        return {
            'success': True,
            'code': 200,
            'message': 'A response was found successfully!',
            'answer': response.get('output_text')
        }


def start_app():
    app.run(host='0.0.0.0', port=3000)


if __name__ == '__main__':
    start_app()
