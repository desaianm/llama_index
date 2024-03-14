from pydantic import BaseModel, Field
from typing import List, Optional
from llama_index.llms.openai import OpenAI
from llama_index.core.indices.struct_store import JSONQueryEngine
import json

resume_schema = {
    "type": "object",
    "properties": {
        "profile_id": {"type": "string"},
        "Name": {"type": "string"},
        "Email": {"type": "string"},
        "links": {
            "type": "array",
            "items": {"type": "string"}
        },
        "Summary": {"type": "string"},
        "Education": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "Institution": {"type": "string"},
                    "Degree": {"type": "string"},
                    "FieldOfStudy": {"type": "string"},
                    "StartDate": {"type": "string"},
                    "EndDate": {"type": "string"},
                    "Achievements": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["Institution", "Degree", "FieldOfStudy", "StartDate", "EndDate"]
            }
        },
        "Skills": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "SkillName": {"type": "string"},
                    "Level": {"type": "string"}
                },
                "required": ["SkillName", "Level"]
            }
        },
        "Projects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "ProjectName": {"type": "string"},
                    "StartDate": {"type": "string"},
                    "EndDate": {"type": "string"},
                    "Responsibilities": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["ProjectName", "StartDate", "EndDate", "Responsibilities"]
            }
        },
        "Experience": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "CompanyName": {"type": "string"},
                    "Role": {"type": "string"},
                    "Location": {"type": "string"},
                    "StartDate": {"type": "string"},
                    "EndDate": {"type": "string"},
                    "Responsibilities": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["CompanyName", "Role", "StartDate", "EndDate", "Responsibilities"]
            }
        },
        "Activities": {
            "type": "array",
            "items": {"type": "string"}
        },
        "Interests": {
            "type": "array",
            "items": {"type": "string"}
        },
        "AdditionalInformation": {"type": "string"}
    },
    "required": ["profile_id", "Name", "Email", "Summary", "Education", "Skills", "Projects", "Experience"]
}

# Define Pydantic models for each section of the resume
class SummaryModel(BaseModel):
    content: str = Field(description="Summary of the individual's professional background")

class EducationModel(BaseModel):
    content: str = Field(description="Educational background details")

class WorkExperienceModel(BaseModel):
    content: str = Field(description="Work experience details")

class ProjectsModel(BaseModel):
    content: str = Field(description="Project involvements and contributions")

class SkillsModel(BaseModel):
    content: str = Field(description="Skills and competencies")

class CertificationsModel(BaseModel):
    content: str = Field(description="Certifications and accreditations")

class ActivitiesModel(BaseModel):
    content: str = Field(description="Extracurricular activities and involvements")

class InterestModel(BaseModel):
    content: str = Field(description="Interests and hobbies")

# Overall model that includes all sections
class ResumeResponseModel(BaseModel):
    Summary: SummaryModel
    Education: EducationModel
    WorkExperience: WorkExperienceModel
    Projects: ProjectsModel
    Skills: SkillsModel
    Certifications: CertificationsModel
    Activities: ActivitiesModel
    Interest: InterestModel

# Load the resume JSON data
with open('llama_index/files/resume.json', 'rb') as file:
    resume_data = json.load(file)

# Load the job posting for context (optional)
with open("llama_index/files/posting.txt") as file:
    posting = file.read()

# Initialize the language model
llm = OpenAI(model="gpt-3.5-turbo")

# Initialize the JSONQueryEngine with the resume data
json_query_engine = JSONQueryEngine(
    json_schema = resume_schema,json_value=resume_data, llm=llm)

queries = f"match each sections in resume data with below job posting and suggest what can improved  in each section : {posting}"
    
# Example query for improvement suggestions
query_result = json_query_engine.query(queries)

strres = str(query_result)

print(query_result)

# Parsing the JSON result into the structured Pydantic model
# Assuming the query_result structure matches the ResumeResponseModel

