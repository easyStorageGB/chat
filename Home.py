import streamlit as st, pathlib, os
from utilities import get_products, aichat
folder = pathlib.Path(__file__).parent.resolve()

st.set_page_config(page_title="Chatbots",  page_icon="🚀",)
st.write("# 👋 Welcome to Receipt Bot!👋")
st.markdown(
    """

#### 🚀Intelligent Bookkeeping and Document Management Hub🍨


"""
)

# st.sidebar.title("Store Spark")
st.sidebar.image(f"{folder}/resources/sslogo.png", use_column_width=True)

with st.sidebar:
    # store_link = st.text_input("Enter Your Store URL:",   value="http://hypech.com/StoreSpark", disabled=True, key="store_link")
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    # "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-0125"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system",      'content': f"""
            You are ShopBot, an AI assistant for  easyStorage service. 

            Your role is to assist customers in offering various charging and space schedules, providing information, and guiding them through the order process. 

            Be friendly and helpful in your interactions.

            We operate over 85% of the UK and we are adding new locations periodically. Here’s a list of some of the larger towns and cities we cover. Or enter your postcode here to receive a detailed storage quote.

            If you receive an alert, it may mean we do not operate in your area just yet but please call our Storage Solutions Specialists for further information even if your collection address isn’t covered, where you want to store might be.

            Feel free to ask customers about their preferences, recommend products, and inform them about any ongoing promotions.

            The Current various charging and space schedules List is limited as below:

            ```{get_products()}```

            Make the shopping experience enjoyable and encourage customers to reach out if they have any questions or need assistance.
            """})
    st.session_state.messages.append({"role": "assistant",   "content": "How May I Help You Today💬?"})


# Display chat messages from history on app rerun
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("💬"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    else: 
        try:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                stream = aichat(messages = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],openai_api_key=openai_api_key)
                response = st.write_stream(stream)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        except:
            st.info("Invalid OpenAI API key. Please enter a valid key to proceed.")