# Sales Assistant Agent

## Overview
The Sales Assistant Agent is a Streamlit-based application powered by Groq AI. This tool helps users analyze business data, compare competitors, and generate actionable insights in real time.

## Features
- Analyze company data and extract insights.
- Compare products with competitors and identify strengths/weaknesses.
- Summarize public statements from key company leaders.
- Suggest actionable recommendations for competitive improvement.
- Allow users to upload documents (PDF, DOCX, TXT) for parsing.


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/sales-assistant-agent.git

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Add your API keys to secrets.toml:

    GROQ_API_KEY = "your_groq_api_key"

    TAVILY_API_KEY = "your_tavily_api_key"


## Usage

1. Run the application:
    ```bash
    streamlit run app.py

2. Fill out the input form with the required details or upload a document.

3. View the insights and download them as a PDF.

