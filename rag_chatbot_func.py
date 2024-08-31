import os 

from pathlib import Path
from dotenv import load_dotenv
from utils import get_doc_tools


from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex
from llama_index.core.agent import AgentRunner
from llama_index.core.objects import ObjectIndex
from llama_index.core.agent import FunctionCallingAgentWorker


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def ChatBot() : 
    files = [
        "data/Apple_Vision_Pro_Privacy_Overview.pdf",
        "data/law-enforcement-guidelines-us.pdf",
        
    ]
    # webpages scraped using webscrapper.py - to be combined
    webpages = [("data/vision_pro_webpage" , "apple_vision_pro")]

    files_to_tools_dict = {}
    for file in files:
        print(f"Getting tools for file: {file}")
        vector_tool, summary_tool = get_doc_tools(file, Path(file).stem)
        files_to_tools_dict[file] = [vector_tool, summary_tool]

    for page,name in webpages:
        print(f"Getting tools for page: {page}")
        vector_tool, summary_tool = get_doc_tools(page, name)
        files_to_tools_dict[page] = [vector_tool, summary_tool]

    print(files_to_tools_dict)

    llm = OpenAI(model="gpt-3.5-turbo")
    all_tools = [t for file in files for t in files_to_tools_dict[file]]

    # defining an "object" index and retriever over these tools
    obj_index = ObjectIndex.from_objects(
        all_tools,
        index_cls=VectorStoreIndex,
    )
    obj_retriever = obj_index.as_retriever(similarity_top_k=3)
    agent_worker = FunctionCallingAgentWorker.from_tools(
        tool_retriever=obj_retriever,
        llm=llm, 
        system_prompt=
        """
        You are an Sales Agent tasked with answering questions based on a set of products related to Apple Inc. Always use the provided tools to gather information from these files to ensure accurate and relevant responses. Do not rely on any prior knowledge or external sources. 

        Your responsibilities include:
        1. Using the tools to extract information from the given files.
        2. Ensuring that answers are directly supported by the content of these files.
        3. Avoiding assumptions or external knowledge that is not present in the files.
        4. Providing clear, concise, and factual responses based on the file contents.
        5. Trying to sell the project, sounding pursuasive but precise

        Remember, the tools are designed to help you retrieve and interpret the information needed to answer queries about Apple Inc.
        """,
        verbose=False
    )
    agent = AgentRunner(agent_worker)

    # response = agent.query(
    #     "How does Apple Vision Pro ensure user privacy when using advanced features like eye-tracking and spatial computing?"
    # )
    return agent


    """ 
        You are an agent designed to answer queries over a set of given files related to AppleInc.
        Please always use the tools provided to answer a question. Do not rely on prior knowledge.
        # """