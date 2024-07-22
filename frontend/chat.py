import streamlit as st
import requests




def app():
    st.title("Chat Page")

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if prompt := st.chat_input('Votre question ici?'):
        with st.chat_message('user'):
            st.markdown(f':violet[{prompt}]')

        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.spinner('En cours...'):
            json_response = requests.post('http://127.0.0.1:3000/api/v1/questions', json={'content': prompt})

            if json_response and json_response.status_code == 200:
                answer = f'{json_response.json() and json_response.json().get('answer') or ''}'
            else:
                answer = f'Nous ne trouvons pas de reponse appropriée a vitre demande'

            with st.chat_message('ai'):
                st.markdown(f':green[{answer}]')
            st.session_state.messages.append({'role': 'ai', 'content': answer})
