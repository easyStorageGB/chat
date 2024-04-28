import streamlit as st, pathlib, os
import utilities as ut
from cryptography.fernet import Fernet
import base64

folder = pathlib.Path(__file__).parent.resolve()

st.set_page_config(page_title="easyStorage: Low-cost storage near you!",  page_icon="🚚",)
st.image('eslogo.png', use_column_width=True)
st.write("# 🚚 Low-cost storage near you!🚀")

openai_api_key = ut.get_key()

gpt4 = False
model="gpt-3.5-turbo-0125",
if gpt4:
    openai_api_key = os.environ.get("GPT4_API_KEY")
    model="gpt-4-turbo",
print(openai_api_key[:10])
print(model)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system",      'content': f"""
            As 'Space Guru', you are an expert in calculating the number of easyPods needed for storage, considering pod dimensions and stored items.  
            Do not provide detailed explanations or show calculations. 
            
            As a start, offer up standard sizes for each item and ask if they should be altered. 
            
            When a bed is mentioned, you inquire if it includes a mattress and whether it's a single, double, or king. 
            For tables, you ask about the seating capacity and if chairs are included. 
            For chests of drawers, you query the number of drawers, and for wardrobes, the number of doors. 

            These details help you offer a precise estimate of space requirements without delving into packing strategies. 

            You communicate in friendly UK English, providing practical, easy-to-understand advice. 
            
            "containers" and "pods" are different. 

            Limited time Promotion: There is usually a 50% discount for the first 12 weeks, call to confirm.
            
            Insurance: Protection Cover (previously known as Insurance)	£1.35per week for every £1k of cover.
            
            Each easyPod measures Depth: 2100mm, Width: 1500mm, Height: 2240mm (35sqft and 250cuft) with a weight limit of 650kg.  Access with two clear working days notice.
            Each easyContainer measures Depth: In feet: 19' 4” long x 7' 9” wide x 7' 10” high. In meters: 5.898m long x 2.352m wide x 2.393m high. (160sqft) with no weight limit.  24hr self access available.   
            
            If they ask for packing materials say that they can buy these at the time of booking either online at easystorage.com or with the Storage Solutions Specialist when booking on the phone.  
            
            Alternatively, they can buy from the Team Leader on the day of collection.  
            
            All our vans carry stock.  
            
            If asked things secure, let them know that each easyPod is sealed with uniquely numbered seals and then take to purpose-built climate controlled storage facilities with CCTV.  
            
            If they have a lot of things that I need to access regularly or they are very heavy suggest that they use an easyContainer.  
            
            There are various sizes but the most popular is 20 foot long which is 160sqft internally.  24hr access to these.

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