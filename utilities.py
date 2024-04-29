import requests, openai, streamlit as st, pymongo, base64
from tenacity import retry, wait_random_exponential, stop_after_attempt
from cryptography.fernet import Fernet

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def aichat(messages, openai_api_key):
    try:
        client = openai.OpenAI(api_key = openai_api_key)
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-0125",
            max_tokens=2024,
            stream=True,
        )
        print(response)
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def get_products():
    # url = "https://hypech.com/StoreSpark/product_short.json" 
    url = "https://hypech.com/StoreSpark/services.json"
    response = requests.get(url)     
    if response.status_code == 200:  
        data = response.text                  
        return data
    else:
        print(f"The store is closed：{response.status_code}")    


def get_item_sizes():
            # ```{ut.get_item_sizes()}```
            # ```{ut.get_packing_material_charges()}```
            # ```{ut.get_pod_container_prices()}```
    url = "https://hypech.com/StoreSpark/easystorage/item_sizes.json"
    response = requests.get(url)     
    if response.status_code == 200:  
        data = response.text                  
        return data
    else:
        print(f"The store is closed：{response.status_code}")    

def get_packing_material_charges():
    url = "https://hypech.com/StoreSpark/easystorage/packing_material_charges.json"
    response = requests.get(url)     
    if response.status_code == 200:  
        data = response.text                  
        return data
    else:
        print(f"The store is closed：{response.status_code}")    

def get_pod_container_prices():
    url = "https://hypech.com/StoreSpark/easystorage/pod_container_prices.json"
    response = requests.get(url)     
    if response.status_code == 200:  
        data = response.text                  
        return data
    else:
        print(f"The store is closed：{response.status_code}")    

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
#    return client.embeddings.create(input = [text], model=model).data[0].embedding

# text = "test embedding"
# embeddings = get_embedding(text)

def get_key():
    uri = st.secrets["MONGO_URI"]
    
    @st.cache_resource
    def init_connection():
        return pymongo.MongoClient(uri)

    client = init_connection()

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        mydatabase = client.easystorage
        mycollection = mydatabase.openai
        query = {"0.name": "key"}
        result = mycollection.find_one(query)

        # Check if the document was found
        openai_api_key = None
        if result:
            # Extract the value
            encrypted_key = result['0']['value']
            print("Retrieved value:", encrypted_key[:20])
            st_key = st.secrets["FERNET"]
            key_bytes = base64.urlsafe_b64decode(st_key)
            cipher_suite = Fernet(key_bytes)
            openai_api_key = cipher_suite.decrypt(encrypted_key).decode()

        else:
            print("Document not found.")
            
        return openai_api_key
    
    except Exception as e:
        print(e)

def get_prompt():
    uri = st.secrets["MONGO_URI"]
    
    @st.cache_resource
    def init_connection():
        return pymongo.MongoClient(uri)

    client = init_connection()
    content = "default"

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        mydb = client.easystorage
        myco = mydb.esprompt
        query = {"item" : "prompt"}
        result = myco.find_one(query)

        # Check if the document was found
        if result:
            content = result.get("content", None)
        else:
            print("Document not found.")
        return content
    
    except Exception as e:
        print(e)