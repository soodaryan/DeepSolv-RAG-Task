<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1>DeepSolv RAG Project 🚀</h1>
    <h2>Overview 📝</h2>
    <p>This project implements a Retrieval-Augmented Generation (RAG) system with a focus on handling unstructured data and providing a user-friendly interface.</p>
    <h2>Implementation Details 🔧</h2>
    <ol>
        <li><strong>RAG Implementation:</strong>
            <ul>
                <li><strong>Language Model:</strong> Utilized OpenAI's GPT-3.5 turbo as the LLM for generating responses. 🤖</li>
                <li><strong>RAG Framework:</strong> Leveraged LlamaIndex to integrate and retrieve relevant information. 📚</li>
            </ul>
        </li>
        <li><strong>Unstructured Data Handling:</strong>
            <ul>
                <li><strong>PDF Data Extraction:</strong> Implemented RAG on data extracted from a PDF document titled <em>"Apple Vision Pro Privacy Overview"</em>. This involved parsing and processing the document to create a structured knowledge base. 📄</li>
            </ul>
        </li>
        <li><strong>Web Scraping:</strong>
            <ul>
                <li><strong>Website Data Collection:</strong> Used BeautifulSoup and LangChain to scrape data from the official Apple Vision Pro website. This data was then integrated into the RAG system to enrich the knowledge base. 🌐</li>
            </ul>
        </li>
        <li><strong>Web Interface:</strong>
            <ul>
                <li><strong>UI Development:</strong> Created an interactive web UI using Streamlit to allow users to interact with the RAG system seamlessly. 🖥️</li>
            </ul>
        </li>
    </ol>
    <h2>How to Run 🏃‍♂️</h2>
    <ol>
        <li><strong>Clone the Repository:</strong>
            <pre><code>git clone https://github.com/soodaryan/DeepSolv-RAG-Task.git
cd DeepSolv-RAG-Task</code></pre>
        </li>
        <li><strong>Install Dependencies:</strong>
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li><strong>Run the Application:</strong>
            <pre><code>streamlit run app.py</code></pre>
        </li>
        <li><strong>Environment Variables:</strong> Ensure you set up necessary environment variables for API keys and database connections. 🔑</li>
    </ol>
    <h2>Final Submission 🎯</h2>
    <ul>
        <li><strong>Code Repository:</strong> <a href="https://github.com/soodaryan/DeepSolv-RAG-Task">Link to GitHub repository</a></li>
        <li><strong>Video Recording:</strong>
        [![Watch the video](images/Screenshot 2024-08-31 at 8.33.34 PM.png)](https://raw.githubusercontent.com/yourusername/yourrepository/main/assets/video.mp4)
    /li>
    </ul>
    <h2>Notes 📋</h2>
    <p>Create a .env file and add your OPENAI API KEY to use the chatbot.</p>
    <p>Ensure you have the required access to APIs and services used in this project.</p>
    <p>Review the <code>requirements.txt</code> for all dependencies and their versions. 📜</p>
    <h2>Acknowledgments 🙏</h2>
    <p>Thanks to the open-source libraries and tools used in this project, including OpenAI, LlamaIndex, BeautifulSoup, LangChain, and Streamlit.</p>
    <h2>License 📜</h2>
    <p>This project is licensed under the MIT License - see the <a href="LICENSE">LICENSE</a> file for details.</p>
</body>
</html>
