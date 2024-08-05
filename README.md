SUMMARY:

Have developed a "Rule-Based AI chatbot" utilizing Natural Language Processing(NLP) techniques to handle user interactions. The core of the system leverages the tokenization (splits a given text into individual words or tokens), stopwords (to remove pronouns,verbs) and stemmer (to reduce words to their root form) concepts from NLTK (Natural Language Toolkit) package in Python to process and analyze text.

The chatbot is designed to read user questions and match them with predefined responses stored in a JSON file. The project also incorporates a Streamlit app to provide a user-friendly interface, allowing users to input questions and receive relevant answers dynamically based on the data in the JSON file.

RUN COMMANDS:

Streamlit run command - streamlit run C:\Users\765727\WebdriverIO\python\streamlitApp.py
Python run command - C:/Users/765727/AppData/Local/Programs/Python/Python312/python.exe c:/Users/765727/WebdriverIO/python/downloadDependency.py

STEPS TO SETUP THIS PROJECT:

Install python
In Environment Variables, Under User Variables add "C:\Users\765727\AppData\Local\Programs\Python\Python312\Scripts\
C:\Users\765727\AppData\Local\Programs\Python\Python312\" in path variables placing these as first 2 paths
python --version = Python 3.12.4
pip install streamlit
pip install nltk
Then Python Run command pointing to downloadDependency.py
