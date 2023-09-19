# Import necessary modules from the IBM Watson Machine Learning SDK
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models import Model

# Import necessary modules from the langchain package
from langchain import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain


# Set up the API key and project ID for IBM Watson 
watsonx_API = ""
project_id= ""

# Set up the credentials for accessing IBM Watson
credentials = {
    'url': "https://us-south.ml.cloud.ibm.com",
    'apikey' : watsonx_API
}

# Set up parameters for the generation of text, including various settings such as the maximum and minimum number of new tokens to generate and the temperature
params = {
    GenParams.MAX_NEW_TOKENS: 100,
    GenParams.TEMPERATURE: 0.5,
}

# Create two prompt templates: one for generating a random question about a given topic, and another for answering a given question
pt1 = PromptTemplate(
    input_variables=["topic"],
    template="Generate a random question about {topic}: Question: ")
pt2 = PromptTemplate(
    input_variables=["question"],
    template="Answer the following question: {question}")

# Set up the LLAMA2 model with the specified parameters and credentials
LLAMA2_model = Model(
    model_id= 'meta-llama/llama-2-70b-chat',
    credentials=credentials,
    params=params,
    project_id=project_id)

# Create a Watson LLM instance with the LLAMA2 model
LLAMA2_model_llm = WatsonxLLM(model=LLAMA2_model)

# Set up the FLAN T5 model with the specified credentials
flan_t5_model = Model(
    model_id="google/flan-t5-xxl",
    credentials=credentials,
    project_id=project_id)

# Create a Watson LLM instance with the FLAN T5 model
flan_t5_llm = WatsonxLLM(model=flan_t5_model)

# Create an LLM chain with the LLAMA2 model and the first prompt template
prompt_to_LLAMA2 = LLMChain(llm=LLAMA2_model_llm, prompt=pt1)

# Create an LLM chain with the FLAN T5 model and the second prompt template
flan_ul2_to_flan_t5 = LLMChain(llm=flan_t5_llm, prompt=pt2)

# Create a simple sequential chain with the two previously created LLM chains and set the verbosity to true
qa = SimpleSequentialChain(chains=[prompt_to_LLAMA2, flan_ul2_to_flan_t5], verbose=True)

# Run the chain with the input "cat", which will generate a random question about "cat" and then answer that question
qa.run("cat")
