import os
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    SummaryIndex,
    StorageContext,
    load_index_from_storage,
)
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core.vector_stores import MetadataFilters, FilterCondition
from typing import List, Optional
from pathlib import Path
from typing import List, Optional
import bs4
from dotenv import load_dotenv


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")



PERSIST_DIR = "./storage"

loader=WebBaseLoader(web_paths=("https://www.apple.com/apple-vision-pro/",),
                     bs_kwargs=dict(parse_only=bs4.SoupStrainer(
                         name=['p', 'h3']

                     )))

text_documents=loader.load()


text_file = open("data/vision_pro_webpage", "w+")
text_file.write(text_documents[0].page_content)
text_file.close()



documents = SimpleDirectoryReader(input_files=["data/vision_pro_webpage"]).load_data()
splitter = SentenceSplitter(chunk_size=1024)
nodes = splitter.get_nodes_from_documents(documents)
vector_index = VectorStoreIndex(nodes)

# Create and save the index
vector_index.storage_context.persist(persist_dir=PERSIST_DIR)

# splitter = SentenceSplitter(chunk_size=1024)
# nodes = splitter.get_nodes_from_documents(text_documents)

# cleaned_documents = [Document(page_content=doc.page_content) for doc in text_documents]


# vector_index = VectorStoreIndex(nodes)
# vector_index.storage_context.persist(persist_dir=PERSIST_DIR)
