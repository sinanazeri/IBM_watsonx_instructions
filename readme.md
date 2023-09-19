# Introducting IBM watsonx.ai API

Watsonx is an AI and data platform with a set of AI assistants designed to help you scale and accelerate the impact of AI with trusted data across your business. The core components include a studio for new foundation models, generative AI, and machine learning.


### The watsonx.ai Interface:
IBM WatsonX.ai facilitates the use of various state-of-the-art large language models (LLMs), including google/flanXXL and Meta/LLAMA2. Users can train, tune, and deploy their own generative AI models seamlessly. The platform features the ‘Prompt Lab’, which is ideal for prompt engineering, and the ‘AutoAI’, a tool that assists in building customized machine learning solutions. Additionally, it provides integrated notebooks for coding and data visualization tools to enhance your analysis and insights.

## The watsonx.ai API
The ibm-watson-machine-learning Python library allows you to work with IBM Watson Machine Learning services. You can train, store, and deploy your models, score them using APIs, and finally integrate them with your application development (documentation).

From my experience 👨🏻‍💻: It is amazingly fast and reliable, once you set it up.

The package can be installed with pip:

```bash
pip install ibm-watson-machine-learning
```

Running a simple QA chat with AI (LLAMA2):

Please note that to run this code you need to have Watsonx_API key and Project_id , ⬇scroll down⬇ to see how to get them.

```python
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods

# Set up the API key and project ID for IBM Watson 
watsonx_API = "" # below is the instruction how to get them
project_id= "" # like "0blahblah-000-9999-blah-99bla0hblah0"

generate_params = {
    GenParams.MAX_NEW_TOKENS: 250
}

model = Model(
    model_id = 'meta-llama/llama-2-70b-chat', # you can also specify like: ModelTypes.LLAMA_2_70B_CHAT
    params = generate_params,
    credentials={
        "apikey": watsonx_API,
        "url": "https://us-south.ml.cloud.ibm.com"
    },
    project_id= project_id
    )

q = "How to be happy?"
generated_response = model.generate(prompt=q)
print(generated_response['results'][0]['generated_text'])
```

### Sign Up and Authentication

An IBM Cloud API key is required to authenticate when using Watson API. Users may obtain this key by first signing up for IBM Cloud at https://cloud.ibm.com/registration and then generating an API key at **https://cloud.ibm.com/iam/apikeys**. Be sure to write your API key down somewhere right after you create it, because you won't be able to see it again!

For your credentials to work with watsonx API, you need an API key and a project ID. Since watsonx is an IBM Cloud service, an API key is required when accessing from the outside. After you sign up and sign in to [IBM watsonx](https://dataplatform.cloud.ibm.com/registration/stepone?context=wx&apps=data_science_experience,watson_data_platform,cos) and [create a project](https://dataplatform.cloud.ibm.com/projects/?context=wx), you can follow the below demonstration to create/get your [IBM Cloud user API key](https://cloud.ibm.com/iam/apikeys).

![Getting IBM cloud user API key](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-GPXX0PPIEN/ezgif.com-video-to-gif.gif)
Next, you need to create/get a project ID for your own watsonx.ai project. Go into your own project on [watsonx.ai](https://dataplatform.cloud.ibm.com/projects/?context=wx) and open `Management` > `General` in the management console to find the project ID like below:


![Getting IBM watsonx project ID](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-GPXX0PPIEN/createProject.gif)


--------

After you create a project, you can go to the project’s `Manage` tab > select the `Services and integrations` page > click `Associate Service` > add the `Watson Machine Learning` service to it.

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-GPXX0PPIEN/associate.gif)


OR

In order to use the API, we also need a project ID. To obtain one, we must create a project in IBM Cloud. Navigate to https://dataplatform.cloud.ibm.com/projects/ and create a new project by clicking on "New Project" and then "Create a New Project". Give your project a name and click "Create" on the bottom left corner. Once you do so, you should automatically be redirected to your project dashboard. You may find your project ID in the address bar in the following format:

```
https://dataplatform.cloud.ibm.com/projects/YOUR-PROJECT-ID?context=wx
```

Once you have your API key and project ID, you can start using Watson API!

## Using watsonx API For Langchain 🦜
Watsonx API can be utilized as LLM for langchain. for example, this script utilizes the IBM Watson Machine Learning to create a question-answering chain (from langchain) using two different models: the LLAMA2 model and the FLAN T5 model.

Firstly, setting up the authentications (assuming you already pip install langachain):

```python
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
```
Secondly, setting up the LLMs (LLAMA2 and FLAN_T5) with promptTemplateform langchain:

```python
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
```

Finally, the instances of LLAMA2_model_llm and flan_t5_llm can be utilized as llm for lanchain.

```python
# Create an LLM chain with the LLAMA2 model and the first prompt template
prompt_to_LLAMA2 = LLMChain(llm=LLAMA2_model_llm, prompt=pt1)

# Create an LLM chain with the FLAN T5 model and the second prompt template
flan_ul2_to_flan_t5 = LLMChain(llm=flan_t5_llm, prompt=pt2)

# Create a simple sequential chain with the two previously created LLM chains and set the verbosity to true
qa = SimpleSequentialChain(chains=[prompt_to_LLAMA2, flan_ul2_to_flan_t5], verbose=True)

# Run the chain with the input "cat", which will generate a random question about "cat" and then answer that question
qa.run("cat")
```







