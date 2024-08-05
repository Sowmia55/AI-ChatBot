from typing import List
from dataclasses import dataclass
import streamlit as st
import os
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import json


@dataclass
class Rule:
    pattern: str
    response: str


@dataclass
class RulesData:
    rules: List[Rule]


# Function to tokenize_removeStopWords_stem_input

def tokenize_removeStopWords_stem_input(text):
    # Initialize the stemmer and get the stop words
    stemmer1 = SnowballStemmer('english')
    stop_words1 = set(stopwords.words("english"))
    # Tokenize the input text
    tokens = word_tokenize(text.lower())
    # Remove stop words and stem the remaining tokens
    processed_tokens = [stemmer1.stem(word)
                        for word in tokens if word not in stop_words1]
    return processed_tokens

# Function to tokenize_removeStopWords_stem_pattern

def tokenize_and_stem_pattern(data):
    stemmer2 = SnowballStemmer('english') 
    rules = data["rules"]      
    tokenized_stemmed_pattern = [([stemmer2.stem(word) for word in word_tokenize(rule["pattern"].lower())], rule["responses"])
                                for rule in rules]
    return tokenized_stemmed_pattern

# Function to get array of json file names

def get_json_file_names():
    files = os.listdir("resources/")
    json_files= [os.path.splitext(file)[0]
                  for file in files if
                  file.endswith('.json')]
    return json_files

# Function to compare the tokenized_input against tokenized_pattern and print the response

def process_and_print_responses(input_words, pattern_words):
    count= 0
    for pattern_tokens, responses in pattern_words:
        if all(token in pattern_tokens for token in input_words):
            st.write(f"___Matched Question:___ {' '.join(pattern_tokens)}")
            # prints all responses
            for index, response in enumerate(responses, start=1):
                st.write(f"___Response {index} :___ {response}")
            # prints random response mapped in respose array
            # st.write(random.choice(responses))
            count= count + 1
    if count == 0:
        st.write("Sorry I cannot understand the question")

# Function to print answer with the process of stemming

def process_and_print_responses_strict(input_words, pattern_words):
    count = 0
    for pattern_tokens, responses in pattern_words:
        if any (token in pattern_tokens for token in input_words):
            st.write(f"___Matched Question:___ {' '.join(pattern_tokens)}")
            # prints all responses
            for index, response in enumerate(responses, start=1):
                st.write(f"___Response {index} :___ {response}")
            # prints random response mapped in respose array
            # st.write(random.choice(responses))
            count= count + 1
    if count == 0:
        st.write("Sorry I cannot understand the question")
                           
# Function to handle file upload and update dropdown

def handle_file_upload(uploaded_file):
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".json"):
                        st.session_state.existingModules = get_json_file_names()
            module_name= os.path.splitext(uploaded_file.name)[0]
            if module_name not in st.session_state.existingModules:
                file_path = f"resources/{uploaded_file.name}"
                with open(file_path, "wb") as file:
                                        file.write(uploaded_file.getvalue())
                st.success("File uploaded successfully!")
            else:
                st.error(
                    "File name already exist. If not a duplicate file, please upload with an alternative file name.")
                    # Update drop down options
            if "modules" not in st.session_state:
                    st.session_state.existingModules = get_json_file_names()
                    st.session_state.modules = []
            if uploaded_file.name.endswith(".json"):
                module_name = os.path.splitext(uploaded_file.name)[0]
                if module_name not in st.session_state.existingModules:
                    st.session_state.modules.append(module_name)
                    st.session_state.modules.sort()
                else:
                    st.error("Choose a JSON file to upload")

if "page" not in st.session_state:
    st.session_state.page= "home"

if st.session_state.page == "home":
    # header
    st.header("Rule-Based AI chatbot using NLP")
    # description
    st.subheader("Welcome to offline support")
    st.sidebar.title("Please upload your JSON here")
     # Upload resources button
    if st.sidebar.button("Upload JSON"):
        st.session_state.page= "upload"
        st.experimental_rerun()
    # dropdown to choose module
    moduleName= st.selectbox(
        'Choose Module', options =[element.capitalize() for element in get_json_file_names()])
    # get user question
    user_question = st.text_input(
        f"Ask your query in {moduleName} module")
        # loading json file in read mode based on module choosed in drop down
    with open(f'resources/{moduleName}'+'.json', 'r') as file:
        data: RulesData= json.load(file)        

        col1, col2= st.columns(2)
        with col2:
            if st.button("Get Partial Match Results"):
                if user_question:
                    process_and_print_responses(tokenize_removeStopWords_stem_input(user_question),
                                             tokenize_and_stem_pattern(data))
        with col1:
            if st.button("Get Exact Match Results"):
                if user_question:
                    process_and_print_responses_strict(tokenize_removeStopWords_stem_input(user_question),
                                                    tokenize_and_stem_pattern(data))

elif st.session_state.page == "upload":
    st.header("Upload JSON File")
    if st.button("Back to home page"):
        st.session_state.page= "home"
        st.experimental_rerun()
    uploaded_file= st.file_uploader("Choose a JSON file", type="json")
    if st.button("Upload"):
        handle_file_upload(uploaded_file)
    st.write("**Your JSON should be in below format,**")
    st.write("""    
        
        {

        "rules": [

        {

        "pattern": "How many types of coverages do we have",

        "responses": ["Medical, Dental and more"]

        },

        {

        "pattern": "How to find if a coverage is active or termed",

        "responses": ["From Customer profile API"]

        }

        ]

        }
        
         """)
