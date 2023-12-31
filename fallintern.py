import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import streamlit as st
from pydantic import BaseModel
from typing import Type
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate 
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import BaseTool
from langchain.schema import SystemMessage

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

llm = ChatOpenAI(model_name='gpt-3.5-turbo-1106')

def search(query: str) -> str:
    """Search Google using the serper.dev API and return the results."""
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json={"q": query})
    return response.text

def scrape_website(objective: str, url: str) -> str:
    """Scrape a website and summarize its content if it's too large."""
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }
    post_url = f"https://chrome.browserless.io/content?token={BROWSERLESS_API_KEY}"
    response = requests.post(post_url, headers=headers, json={"url": url})

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        # Summarize content if it exceeds 10,000 characters
        return summary(objective, text) if len(text) > 10000 else text

    raise ValueError(f"HTTP request failed with status code {response.status_code}")

def summary(objective: str, content: str) -> str:
    """Generate a summary of the given content based on the provided objective."""
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    map_prompt = """
    Write a summary of the following text for {objective}:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text", "objective"])
    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=True
    )
    return summary_chain.run(input_documents=docs, objective=objective)

class ScrapeWebsiteInput(BaseModel):
    objective: str  # Objective or task provided by the user
    url: str  # URL of the website to be scraped

class ScrapeWebsiteTool(BaseTool):
    name = "scrape_website"
    description = ("Useful for retrieving data from a website. "
                   "Provide both URL and objective to the function. "
                   "Only use URLs from search results.")
    args_schema: Type[BaseModel] = ScrapeWebsiteInput

    def _run(self, objective: str, url: str) -> str:
        """Execute the tool."""
        return scrape_website(objective, url)

tools = [
    Tool(name="Search", func=search, description="Answer questions using current events/data. Be specific."),
    ScrapeWebsiteTool(),
]

system_message_content = """..."""

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    "system_message": SystemMessage(content=system_message_content),
}

memory = ConversationSummaryBufferMemory(
    memory_key="memory", return_messages=True, llm=llm, max_token_limit=1000)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    agent_kwargs=agent_kwargs,
    memory=memory,
)

def main():
    """Main Streamlit application."""
    st.set_page_config(page_title="Fall Intern", page_icon=":bird:")
    st.header(":globe_with_meridians: Fall Intern")
    st.subheader('Go deeper on topics and questions.')
    query = st.text_input("Research goal")
    st.sidebar.title('About the app')
    st.sidebar.markdown("Fall Intern is a research assistant that will answer your query by searching, scraping and summmarizing real time results from across the web and return a cogent document with citations.")

    if query:
        with st.spinner("Researching..."):
            result = agent({"input": query})
        st.info(result['output'])

if __name__ == '__main__':
     main()