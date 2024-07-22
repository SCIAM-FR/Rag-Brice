import streamlit as st





def app():
    st.title("Chat Page")

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if prompt := st.chat_input('Votre question ici?'):
        with st.chat_message('user'):
            st.markdown(prompt)

        st.session_state.messages.append({'role': 'user', 'content': prompt})

        response = f'Echo: {prompt}'

        with st.chat_message('ai'):
            st.markdown(response)
        st.session_state.messages.append({'role': 'ai', 'content': response})
