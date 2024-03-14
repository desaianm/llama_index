from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.output_parsers import LangchainOutputParser
from llama_index.llms.openai import OpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import json
from llama_index.core.indices.struct_store import JSONQueryEngine

# Assuming your resume is stored in a text format in a directory,
# adjust the path to where your resume file is stored


resume_directory = "llama_index/files/"

with open("llama_index/files/posting.txt") as file:
   posting = file.read() 

# Load the resume document and build an index
documents = SimpleDirectoryReader(resume_directory).load_data()
index = VectorStoreIndex.from_documents(documents)

# Define response schemas for different sections of a resume
response_schemas = [

    ResponseSchema(
        name="Summary",
        description="Suggest what changes or keywords misssing",
    ),
    ResponseSchema(
        name="Education",
        description="Suggest what changes or keywords misssing",
    ),
    ResponseSchema(
        name="Work Experience",
        description="Suggest what changes or keywords misssing",
    ),
    ResponseSchema(
        name="Projects",
        description="Suggest what changes or keywords misssing",
    ),
    ResponseSchema(
        name="Skills",
        description="Suggest what changes or keywords misssing",
    ),
    ResponseSchema(
        name="Certifications",
        description="Suggest what changes or keywords misssing",
    ),
    ResponseSchema(
        name="Activities",
        description="Suggest what changes or keywords misssing",
    ),ResponseSchema(
        name="Interest",
        description="Suggest what changes or keywords misssing",
    )
    
]

# Define the output parser using the response schemas
lc_output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
output_parser = LangchainOutputParser(lc_output_parser)

# Attach the output parser to the LLM (Language Model)
llm = OpenAI(output_parser=output_parser)

# Create a query engine with the indexed resume data and the configured LLM
query_engine = index.as_query_engine(llm=llm)

# Define queries for each section of the resume
queries = [
    f"match and analayze with below job posting : {posting}",
    
]


# Iterate through the queries and obtain structured responses for each section
for query in queries:
    response = query_engine.query(query)
    #print(f"Response: {str(response)}\n")


#response = json.dumps(response)
#summary = response.extra_info["Summary"]
print(response.metadata)
# Note: The actual output will depend on the contents of your resume 
# and the capability of the LLM to parse and understand the document structure.
