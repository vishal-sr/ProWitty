from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.core import PromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core import Settings
from llama_index.core.llms.llm import LLM
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.retrievers.bm25 import BM25Retriever

from data_pipeline import RawData
from aws_service import aws_llm, aws_embed

import phoenix as px
import llama_index.core
llama_index.core.set_global_handler("arize_phoenix")
session = px.launch_app()

class ProWitty:
    def __init__(
            self, 
            llm, 
            embedModel,
            dbLoc = "",
            collectionName = "",
            chatLoc = ""
        ):

        self.embedModel = embedModel
        self.llm = llm
        Settings.llm = self.llm
        Settings.embed_model = self.embedModel

        self.nodes = RawData(
            rawFileStorageDirectory = r"C:\Users\vishal\Documents\AI\ProWitty\storage\files",
            videoFileName = ""
        ).get_nodes()

        self.dbLoc = dbLoc
        self.collectionName = collectionName
        self.chatLoc = chatLoc

    def load(self):
        db = chromadb.PersistentClient(path = self.dbLoc)
        chroma_collection = db.get_or_create_collection(name = self.collectionName)
        vector_store = ChromaVectorStore(chroma_collection = chroma_collection)
        index = VectorStoreIndex.from_vector_store(
            vector_store = vector_store,
            embed_model = self.embedModel
        )
        chatStore = SimpleChatStore.from_persist_path(self.chatLoc)
        return index, chatStore

    def chat_engine(queryEngine, llm, chatStore):
        customPrompt = PromptTemplate("""Given a conversation (between Human and Assistant) and a follow up message from Human, rewrite the message to be a standalone question that captures all relevant context from the conversation and that standalone question can be used to query a vector database to get the relavent data.\n<Chat History>\n{chat_history}\n<Follow Up Message>\n{question}\n<Standalone question>""")

        customChatHistory = chatStore.get_messages("user01") 

        chatEngine = CondenseQuestionChatEngine.from_defaults(
            query_engine = queryEngine,
            condense_question_prompt = customPrompt,
            chat_history = customChatHistory,
            verbose = True,
            llm = llm
        )

        return chatEngine

    def query(self, query_str: str, debug: bool = False):

        index, chatStore = self.load()
        
        base_retriever = index.as_retriever(similarity_top_k = 5)
        bm25_retriever = BM25Retriever.from_defaults(nodes = self.nodes, similarity_top_k = 5)
        retriever = QueryFusionRetriever(
            similarity_top_k = 5,
            num_queries = 4, 
            retrievers = [base_retriever, bm25_retriever],
            mode = "reciprocal_rerank",
        )    
        queryEngine = RetrieverQueryEngine.from_args(retriever)
    
        chat_engine = ProWitty.chat_engine(
            queryEngine = queryEngine,
            llm = self.llm,
            chatStore = chatStore
        )
        
        response = chat_engine.chat(query_str).response

        if debug:
            import time
            while True:
                time.sleep(100)


        return response

if __name__ == "__main__":
    bot = ProWitty(
        llm = aws_llm(),
        embedModel = aws_embed(),
        dbLoc = "storage/vectorDB",
        collectionName = "defaultDB",
        chatLoc = "storage/chat_store.json"
    )
    response = bot.query("What is the purpose of ProWitty?", debug = True)