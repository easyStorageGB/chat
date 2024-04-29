import streamlit as st, pathlib, os
import utilities as ut
from cryptography.fernet import Fernet
import base64

folder = pathlib.Path(__file__).parent.resolve()

st.set_page_config(page_title="easyStorage:Low-cost storage near you!",  page_icon="🚚",)
left_co, cent_co,last_co = st.columns(3)
with left_co:
    st.image('eslogo.png')
# st.write("# Low-cost storage near you!")
st.markdown('# <span style="font-family: Helvetica;">Low-cost storage near you!</span>', unsafe_allow_html=True)

openai_api_key = ut.get_key()

gpt4 = False
model="gpt-3.5-turbo-0125",
if gpt4:
    openai_api_key = os.environ.get("GPT4_API_KEY")
    model="gpt-4-turbo",
# print(openai_api_key[:10])
# print(model)
# print(ut.get_prompt())

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "system",      
        "content": f"""
            ```{ut.get_prompt()}```
            The Current various charging and space schedules List is limited as below:
            ```{ut.get_item_sizes()}```
            ```{ut.get_packing_material_charges()}```
            ```{ut.get_pod_container_prices()}```
            """})
    
    st.session_state.messages.append({"role": "assistant",   "content": "How May I Help You Today💬?"})


# Display chat messages from history on app rerun
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("easyStorage:💬"):
    if not openai_api_key:
        st.info("OpenAI API Key expired.")
    else: 
        try:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                stream = ut.aichat(messages = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],openai_api_key=openai_api_key)
                response = st.write_stream(stream)
                print(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        except:
            st.info("Invalid OpenAI API key. Please enter a valid key to proceed.")