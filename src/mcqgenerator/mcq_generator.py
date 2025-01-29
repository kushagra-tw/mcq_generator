import os,json,traceback, pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging
#importing necessary packages for langchain
from langchain_community.chat_models import ChatOpenAI   
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain



#loading the .env file

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

#defining llm model
llm = ChatOpenAI(openai_api_key=key,model="gpt-3.5-turbo",temperature=0.3)


template = """
Text:{input_text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format response like response_json below and use it as a guide. \
Ensure to make {number} MCQs
### response_json
{response_json} 
"""
quiz_generation_prompt = PromptTemplate(
    input_variables=['input_text', 'number', 'subject', 'tone', 'response_json'],
    template=template
)

#combining llm and prompt
quiz_chain = LLMChain(llm = llm, prompt = quiz_generation_prompt,output_key='quiz',verbose=True)


# #evaluating the mcq

template2 = """
You are an expert english gramarian and writer. Given a Multiple choice quiz for {subject} students. \
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use max of 50 words for complexity.
If the quiz is not at per with cognitive and analytical abilities of the students.\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits with student abilities.
quic mcqs:
{quiz}
"""
quiz_evaluation_prompt = PromptTemplate(input_variables=['subject','quiz'],template=template2)

#combining llm and prompt

evaluation_chain = LLMChain(llm = llm, prompt = quiz_evaluation_prompt,output_key = 'reviews',verbose=True)


# #joining the chains

llm_chain = SequentialChain(chains = [quiz_chain,evaluation_chain],
                            input_variables = ['input_text','number','subject','tone','response_json'],
                            output_variables = ['quiz','reviews'],verbose=True)


 