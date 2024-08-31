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


PERSIST_DIR = "./storage"

def get_doc_tools(
    file_path: str,
    name: str,
):
    """Get vector query and summary query tools from a document with persistence."""

    # Initialize vector_index
    vector_index = None

    # Check if storage already exists
    if not os.path.exists(PERSIST_DIR):
        # Load documents
        print("Creating data base !!")
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        splitter = SentenceSplitter(chunk_size=1024)
        nodes = splitter.get_nodes_from_documents(documents)
        vector_index = VectorStoreIndex(nodes)

        # Create and save the index
        vector_index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:

        print("Using stored data !!")
        # Load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        vector_index = load_index_from_storage(storage_context)

    # If nodes are needed for summary, ensure they are available
    if vector_index is None:
        raise ValueError("VectorStoreIndex is not properly initialized.")

    def vector_query(
        query: str, 
        page_numbers: Optional[List[str]] = None
    ) -> str:
        """Use to answer questions over a given paper.

        Args:
            query (str): the string query to be embedded.
            page_numbers (Optional[List[str]]): Filter by set of pages. Leave as NONE 
                if we want to perform a vector search over all pages. Otherwise, filter 
                by the set of specified pages.
        """
        page_numbers = page_numbers or []
        metadata_dicts = [{"key": "page_label", "value": p} for p in page_numbers]
        
        query_engine = vector_index.as_query_engine(
            similarity_top_k=2,
            filters=MetadataFilters.from_dicts(
                metadata_dicts,
                condition=FilterCondition.OR
            )
        )
        response = query_engine.query(query)
        return response
        
    vector_query_tool = FunctionTool.from_defaults(
        name=f"vector_tool_{name}",
        fn=vector_query
    )
    
    # To create a summary_index, you need nodes, which are part of the documents, not vector_index
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)

    summary_index = SummaryIndex(nodes)
    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",
        use_async=True,
    )
    summary_tool = QueryEngineTool.from_defaults(
        name=f"summary_tool_{name}",
        query_engine=summary_query_engine,
        description=f"Useful for summarization questions related to {name}",
    )

    return vector_query_tool, summary_tool

def clean_text(text: str) -> str:
    """Clean the raw text by removing unnecessary whitespace and new lines."""
    cleaned_text = ' '.join(line.strip() for line in text.split('\n') if line.strip())
    return cleaned_text

# def get_web_scraper_tools(
#     url: str,
#     name: str,
# ):
#     """Get vector query and summary query tools from a web page with persistence."""

#     # Initialize vector_index
#     vector_index = None

#     # Check if storage already exists
#     if not os.path.exists(PERSIST_DIR):
#         print("Creating database from web scraper!")

#         # Load documents from the web
#         loader = WebBaseLoader(
#             web_paths=(url,),
#             bs_kwargs=dict(parse_only=bs4.SoupStrainer(name=['p', 'h3']))
#         )
#         text_documents = loader.load()

#         print(text_documents)
#         # Clean and process documents
#         documents = [Document(text=clean_text(doc.text)) for doc in text_documents]
        
#         # Create nodes from documents
#         splitter = SentenceSplitter(chunk_size=1024)
#         nodes = splitter.get_nodes_from_documents(documents)
        
#         # Create and store the index
#         vector_index = VectorStoreIndex(nodes)
#         vector_index.storage_context.persist(persist_dir=PERSIST_DIR)
#     else:
#         print("Using stored data!")
#         # Load the existing index
#         storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
#         vector_index = load_index_from_storage(storage_context)

#     # Ensure vector_index is properly initialized
#     if vector_index is None:
#         raise ValueError("VectorStoreIndex is not properly initialized.")

#     def vector_query(
#         query: str, 
#         page_numbers: Optional[List[str]] = None
#     ) -> str:
#         """Use to answer questions over a given paper."""
#         page_numbers = page_numbers or []
#         metadata_dicts = [{"key": "page_label", "value": p} for p in page_numbers]
        
#         query_engine = vector_index.as_query_engine(
#             similarity_top_k=2,
#             filters=MetadataFilters.from_dicts(
#                 metadata_dicts,
#                 condition=FilterCondition.OR
#             )
#         )
#         response = query_engine.query(query)
#         return response
        
#     vector_query_tool = FunctionTool.from_defaults(
#         name=f"vector_tool_{name}",
#         fn=vector_query
#     )
    
#     # Create a summary index
#     documents = [Document(text=clean_text(doc.text)) for doc in text_documents]
#     splitter = SentenceSplitter(chunk_size=1024)
#     nodes = splitter.get_nodes_from_documents(documents)
    
#     summary_index = SummaryIndex(nodes)
#     summary_query_engine = summary_index.as_query_engine(
#         response_mode="tree_summarize",
#         use_async=True,
#     )
#     summary_tool = QueryEngineTool.from_defaults(
#         name=f"summary_tool_{name}",
#         query_engine=summary_query_engine,
#         description=f"Useful for summarization questions related to {name}",
#     )

#     return vector_query_tool, summary_tool



# # from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
# # from llama_index.core.node_parser import SentenceSplitter
# # from llama_index.core.tools import FunctionTool, QueryEngineTool
# # from llama_index.core.vector_stores import MetadataFilters, FilterCondition
# # from typing import List, Optional

# # def get_doc_tools(
# #     file_path: str,
# #     name: str,
# # ) -> str:
# #     """Get vector query and summary query tools from a document."""

# #     # load documents
# #     documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
# #     splitter = SentenceSplitter(chunk_size=1024)
# #     nodes = splitter.get_nodes_from_documents(documents)
# #     vector_index = VectorStoreIndex(nodes)
    
# #     def vector_query(
# #         query: str, 
# #         page_numbers: Optional[List[str]] = None
# #     ) -> str:
# #         """Use to answer questions over a given paper.
    
# #         Useful if you have specific questions over the paper.
# #         Always leave page_numbers as None UNLESS there is a specific page you want to search for.
    
# #         Args:
# #             query (str): the string query to be embedded.
# #             page_numbers (Optional[List[str]]): Filter by set of pages. Leave as NONE 
# #                 if we want to perform a vector search
# #                 over all pages. Otherwise, filter by the set of specified pages.
        
# #         """
    
# #         page_numbers = page_numbers or []
# #         metadata_dicts = [
# #             {"key": "page_label", "value": p} for p in page_numbers
# #         ]
        
# #         query_engine = vector_index.as_query_engine(
# #             similarity_top_k=2,
# #             filters=MetadataFilters.from_dicts(
# #                 metadata_dicts,
# #                 condition=FilterCondition.OR
# #             )
# #         )
# #         response = query_engine.query(query)
# #         return response
        
    
# #     vector_query_tool = FunctionTool.from_defaults(
# #         name=f"vector_tool_{name}",
# #         fn=vector_query
# #     )
    
# #     summary_index = SummaryIndex(nodes)
# #     summary_query_engine = summary_index.as_query_engine(
# #         response_mode="tree_summarize",
# #         use_async=True,
# #     )
# #     summary_tool = QueryEngineTool.from_defaults(
# #         name=f"summary_tool_{name}",
# #         query_engine=summary_query_engine,
# #         description=(
# #             f"Useful for summarization questions related to {name}"
# #         ),
# #     )

# #     return vector_query_tool, summary_tool


# import os
# from llama_index.core import (
#     SimpleDirectoryReader,
#     VectorStoreIndex,
#     SummaryIndex,
#     StorageContext,
#     load_index_from_storage,
# )
# from llama_index.core.node_parser import SentenceSplitter
# from llama_index.core.tools import FunctionTool, QueryEngineTool
# from llama_index.core.vector_stores import MetadataFilters, FilterCondition
# from typing import List, Optional

# PERSIST_DIR = "./storage"

# def get_doc_tools(
#     file_path: str,
#     name: str,
# ) -> str:
#     """Get vector query and summary query tools from a document with persistence."""
#     nodes = None
#     # Check if storage already exists
#     if not os.path.exists(PERSIST_DIR):
#         # Load documents
#         documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
#         splitter = SentenceSplitter(chunk_size=1024)
#         nodes = splitter.get_nodes_from_documents(documents)
#         vector_index = VectorStoreIndex(nodes)

#         # Create and save the index
#         vector_index.storage_context.persist(persist_dir=PERSIST_DIR)
#     else:
#         # Load the existing index
#         storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
#         vector_index = load_index_from_storage(storage_context)

#     def vector_query(
#         query: str, 
#         page_numbers: Optional[List[str]] = None
#     ) -> str:
#         """Use to answer questions over a given paper.

#         Args:
#             query (str): the string query to be embedded.
#             page_numbers (Optional[List[str]]): Filter by set of pages. Leave as NONE 
#                 if we want to perform a vector search over all pages. Otherwise, filter 
#                 by the set of specified pages.
#         """
#         page_numbers = page_numbers or []
#         metadata_dicts = [{"key": "page_label", "value": p} for p in page_numbers]
        
#         query_engine = vector_index.as_query_engine(
#             similarity_top_k=2,
#             filters=MetadataFilters.from_dicts(
#                 metadata_dicts,
#                 condition=FilterCondition.OR
#             )
#         )
#         response = query_engine.query(query)
#         return response
        
#     vector_query_tool = FunctionTool.from_defaults(
#         name=f"vector_tool_{name}",
#         fn=vector_query
#     )
    
#     summary_index = SummaryIndex(nodes)
#     summary_query_engine = summary_index.as_query_engine(
#         response_mode="tree_summarize",
#         use_async=True,
#     )
#     summary_tool = QueryEngineTool.from_defaults(
#         name=f"summary_tool_{name}",
#         query_engine=summary_query_engine,
#         description=f"Useful for summarization questions related to {name}",
#     )

#     return vector_query_tool, summary_tool
