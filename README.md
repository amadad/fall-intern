# Fall Intern

## 📖 Overview

Fall Intern is an intelligent, cutting-edge research tool tailored to assist users in diving deep into various topics and questions. Built on the robust foundation of multiple libraries, including Streamlit, BeautifulSoup, the application is designed to fetch, scrape, summarize, and present web content with concision and precision.

- **Efficient Research:** No need to manually sift through countless search results or pages. Get straight to the point with accurate and relevant information.
- **Web Scraping Capabilities:** With the integration of BeautifulSoup, extract valuable data directly from websites, ensuring you're always equipped with the most up-to-date information.
- **Intelligent Summarization:** For content-heavy topics, the application condenses the information, presenting a clear and concise overview without missing out on essential details.
- **Interactive Web Interface:** A user-friendly Streamlit web application ensures a smooth and intuitive experience for all users, regardless of their tech-savviness.

## 🚀 Features

- **Research Goal Input:** Input your research goals or questions and get detailed information on the topic.
- **Web Scraping:** Uses BeautifulSoup to scrape websites.
- **Information Summarization:** If the content is vast, it summarizes the content to give a concise overview.
- **Web Application:** A simple yet powerful web application interface using Streamlit.
- **API Endpoint:** A FastAPI endpoint to get research content programmatically.

## 🔧 Setup

### Prerequisites:
- Python installed on your machine.
- API keys for browserless and serper.

### Steps:
1. Clone the repository.
2. Set up a virtual environment and install the required libraries using pip:
   ```bash
   pip install streamlit BeautifulSoup4 requests fastapi
   ```
3. Set your API keys in the .env file:
   ```env
   BROWSERLESS_API_KEY=your_browserless_api_key
   SERPER_API_KEY=your_serper_api_key
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run your_script_name.py
   ```
5. To run the FastAPI endpoint, uncomment the FastAPI section in the script and then:
   ```bash
   uvicorn your_script_name:app --reload
   ```

## 💻 Usage

### Web Application:
1. Navigate to the Streamlit application in your browser.
2. Enter your research goal or topic in the input box.
3. Wait for the operation to complete.
4. View the summarized research content based on your query.

### FastAPI Endpoint:
- Make a POST request with your research query in the following format:
  ```json
  {
      "query": "Your research topic or question here"
  }
  ```
  The API will return the summarized content of your research topic.

## ⚠️ Notes

- The scraping functionality is designed to work with certain websites. It may not work with sites that have dynamic content rendered via JavaScript unless integrated with solutions like browserless.
- Always respect the terms of service of any website you scrape. Some websites may prohibit scraping or have limitations on access.

## 🙏 Support

If you like this project and find it useful, consider supporting it through donations. Your support will help keep the project running.

[Donate](#)

## 📝 License

This project is open-source. Feel free to use, modify, and distribute it. Ensure to give credit and respect the licenses of the utilized libraries.

## 👥 Contributors

The original project was created by Jason Zhou.

- [Jason Zhou](https://github.com/JayZeeDesign)
