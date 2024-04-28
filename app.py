# from chat_pipeline import ProWitty
# from data_pipeline import DataPipeline
# from aws_service import *

# def initialize_s3():
#     baseLoc = ""
#     import boto3

#     # Configure AWS credentials and region
#     aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
#     aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
#     aws_region = 'us-west-1'  # Change to your AWS region

#     # Create an S3 client
#     s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
#                             aws_secret_access_key=aws_secret_access_key,
#                             region_name=aws_region)

#     # Use the S3 client to list objects in a bucket
#     response = s3_client.list_objects_v2(Bucket='your-bucket-name')
#     print(response)

#     return baseLoc

# if __name__ == "__main__":
#     dp = DataPipeline(
#         rawFileStorageDirectory = r"C:\Users\vishal\Documents\AI\ProWitty\storage\files",
#         videoFileName = ""
#     )
#     nodes = dp.build_and_save()

#     chat = ProWitty(
#         llm = aws_llm(),
#         embedModel = aws_embed(),
#         dbLoc = "storage/vectorDB",
#         collectionName = "defaultDB",
#         chatLoc = "storage/chat_store.json"
#     )

#     print(chat.query("can I get more details on Query execution error in Vector DB ticket?", debug = True))


import streamlit as st
from chat_pipeline import ProWitty
from aws_service import aws_llm, aws_embed

def get_response(query):
    # CALL PROWITTY OBJECT HERE
    bot = ProWitty(
        llm = aws_llm(),
        embedModel = aws_embed(),
        dbLoc = "storage/vectorDB",
        collectionName = "defaultDB",
        chatLoc = "storage/chat_store.json"
    )
    response = bot.query(query)
    return response

st.title("ProWitty")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role":"assistant", "content":"I am your personal assisstant. I have the knowledge of all the provided files. "}]

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything"):

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
        
    response = get_response(prompt)
    with st.chat_message("Ai"):
        st.markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    