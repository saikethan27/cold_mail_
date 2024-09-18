import json
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class llm_trans:
    def __init__(self) -> None:
        self.llm = ChatGroq(
            model="mixtral-8x7b-32768",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"))



    def content_extarct(self,page_data):
        prompt_extract = PromptTemplate.from_template(
                """
                ### SCRAPED TEXT FROM WEBSITE:
                {page_data}
                ### INSTRUCTION:
                The scraped text is from the career's page of a website.
                Your job is to extract the job postings and return them in JSON format containing the 
                following keys: `role`, `experience`, `skills` and `description`.
                Only return the valid JSON.
                ### VALID JSON (NO PREAMBLE):    
                """
        )

        chain_extract = prompt_extract | self.llm

        res=chain_extract.invoke(input={'page_data':page_data})
        res_str=res.content
        parsed_data=json.loads(res_str)
        if isinstance(parsed_data,list) and len(parsed_data)==1:
            parsed_data=parsed_data[0]
        return parsed_data

    def email_content(self,job_des,links):

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Mohan, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Atliq's portfolio: {link_list}
            Remember you are Mohan, BDE at AtliQ. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job_des), "link_list": links})
        return res.content
    
# if __name__== "__main__":
#     print(os.getenv("GROQ_API_KEY"))