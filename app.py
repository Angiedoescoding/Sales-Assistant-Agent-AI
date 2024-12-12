import streamlit as st          # to create the app's frontend
from langchain_groq import ChatGroq         # a class for interacting with the Groq LLM using an API key
from langchain_core.prompts import ChatPromptTemplate           # for creating structured prompts for the LLM
from langchain_core.output_parsers import StrOutputParser       #  to extract output in string format
from langchain_community.tools.tavily_search import TavilySearchResults     # a community tool for searching and retrieving results from a provided URL

# Model and Agent Tools
llm = ChatGroq(
    api_key=st.secrets.get("GROQ_API_KEY"),
    temperature=0.7,  # Balanced creativity
    max_tokens=1500
)

# Sufficient token limit for detailed responses)     # fetching the key stored
search = TavilySearchResults(
    max_results=2,
    tavily_api_key=st.secrets.get("TAVILY_API_KEY")
)     # search tool to retrieve information from a provided URL (max of 3 results)

parser = StrOutputParser()      # to process and format the LLM's output


# Page Header
st.title('Sales Assistant Agent')   # app title
st.markdown('The Assistance Agent powered by Groq.')    # brief description
st.markdown("This tool helps you analyze business data, compare competitors, and generate actionable insights.")


# Sidebar for additional information
with st.sidebar:
    st.markdown("## About")
    st.markdown(
        "This app uses AI to analyze company data, generate insights, and provide suggestions for competitive advantage."
    )
    # Add controls for temperature and max tokens
    st.markdown("### LLM Settings")
    temperature = st.sidebar.slider("Temperature (Creativity)", 0.0, 1.0, 0.5)
    max_tokens = st.sidebar.number_input("Max Tokens (Output Length)", min_value=100, max_value=3000, value=1500)
    st.sidebar.info("""
    - *Temperature:* Higher values increase creativity but may reduce focus. Lower values produce more deterministic and focused outputs.
    - *Max Tokens:* Controls the maximum length of the response.
    """)
    
    # Pass user-defined settings to the LLM
    llm = ChatGroq(
        api_key=st.secrets.get("GROQ_API_KEY"),
        temperature=temperature,
        max_tokens=max_tokens
)
    st.markdown("📧 Contact: support@yayyay.com")
    st.markdown("🔗 [Visit Groq](https://www.groq.com)")


# Data Collection/Input Form
with st.form("company_info", clear_on_submit=True):  # creating a form for company_info and clearing the form after submission
    # collecting the product name, company URL, and a list of competitors from the user and placing in the columns for a better readability

    col1, col2 = st.columns(2)

    with col1:
            product_name = st.text_input(
                "**Product Name** (What product are you selling?):"
            )
            product_category = st.text_input(
                "**Product Category** (e.g., 'Data Warehousing'):"
            )
            company_url = st.text_input(
                "**Company URL** (The URL of the product's company):"
            )

    with col2:
            competitors = st.text_input(
                "**Competitors List** (e.g., Apple, Tesla, Google):"
            )

            target_customer = st.text_input(
                "**Target Customer** (Who are you selling to?):"
            )

            competitors_url = st.text_input(
                "**Competitors URL** (e.g., www.apple.com):"
            )
    
    value_proposition = st.text_input("**Value Proposition** (Summarize the product’s value):")


# Allow users to upload a document for analysis
    uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, or TXT):", type=["pdf", "docx", "txt"])
    if uploaded_file:
        file_contents = uploaded_file.read().decode("utf-8") if uploaded_file.type == "text/plain" else "Content extraction logic here"
        st.markdown("### Uploaded Document Content")
        st.text(file_contents)

# Add the submit button inside the `st.form` block
    submit_button = st.form_submit_button("Generate Insights")


# Processing and Generating Insights for the llm
company_insights = ''   # initializing an empty string to store the results

# Data process
if submit_button:      # adding a button to submit the form
        if product_name and company_url:  # validation step to make sure these two items are provided before proceeding
            with st.spinner('Processing...'):

            # Use search tool to get Company Information
                company_information = search.invoke(company_url)  # calling the search tool to fetch data from the provided company_url and storing the output in the company_information
            #print(company_information)     
            # log the fetched data for debugging purposes

                # st.write("Company Information:", company_information)

            # Prompt Setup - todo: Create prompt <=======
                prompt = f''' 
                Role: You are a Business Analyst Assistant in the company that focuses on making and selling products that make people's life better. Your task is to analyze company data and generate actionable insights. Ensure major parts of the output are bolded for better readability.
                Based on the provided input variables, perform the following tasks:

                1. Company Overview:
                    Provide a brief summary of the company's product: {{product_name}}.
                    Analyze the company's website data ({{company_information}}) and identify:
                        Unique value propositions.
                        Key strengths and potential weaknesses of the company and its product.
                2. Competitive Analysis:
                    Compare the company's product with its competitors ({{competitors}}):
                        Highlight key differentiators.
                        Identify areas where the company excels compared to competitors.
                        Point out areas where competitors may have an advantage.
                3. Key Leaders and Public Statements:
                    List key leaders at the company, especially those quoted in public sources (e.g., press releases, articles) over the last year.
                    Summarize relevant public statements or press releases where key executives (e.g., Chief Data Officer, Chief Compliance Officer) discussed significant topics.
                4. Strategic Insights:
                    For public companies, provide insights from 10-Ks, annual reports, or other relevant documents.
                    Summarize the company's current strategic position and areas for improvement.
                5. Actionable Recommendations:
                    Suggest ways to improve the company's competitive position based on the analysis.
                6. Supporting Resources:
                    Include links to full articles, press releases, or other relevant sources referenced in your analysis.
                
                Input Variables:
                    Product Name: {{product_name}}
                    Company Data: {{company_information}}
                    Competitors: {{competitors}}
                    Product Category: {{product_category}}

            
                '''     # Placeholder for a structured task description for the LLM. You should add content here, such as instructions for generating insights or analyzing competitors =======                 Include the company's website [url] as part of the analysis.

            # Prompt Template
                prompt_template = ChatPromptTemplate([('system', prompt)])      # Wrap the prompt into a reusable template that can be passed to the LLM

            # Chain
                chain = prompt_template | llm | parser      # connects the prompt, LLM, and output parser

            # Result/Insights >> executing the chain using these items
                company_insights = chain.invoke(
                    {
                        "url": company_url, 
                        "company_information": company_information,
                        "product_name": product_name,
                        "competitors": competitors,
                        "product_category": product_category,

                        "competitors_url": competitors_url,
                        "value_proposition": value_proposition,
                        "target_customer": target_customer
                    }
                ) # The result (insights) is stored in company_insights

# Display Insights
with st.expander("View Insights"):
    st.markdown(company_insights)




# Testing the Application
# Use realistic test data:

# Product Name: "SmartHome Assistant"
# Company URL: "https://www.smarthome.com"
# Product Category: "Home Automation"
# Competitors: "Amazon Alexa, Google Nest"
# Competitors URL: "https://www.amazon.com/alexa"
# Value Proposition: "Streamline your life with our eco-friendly home assistant."
# Target Customer: "John Doe, CTO"
