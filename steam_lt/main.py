import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import json
from chroma_db_details import Portfolio
from llm_connector import llm_trans


st.title('Cold_mail processing Application')

st.write("Enter url of job below")

url=st.text_input("Url",value="https://www.amazon.jobs/en/jobs/2713915/software-development-engineer-efa")

if st.button('Get_mail_content'):
    pf=Portfolio()
    pf.load_portfolio()
    loader = WebBaseLoader(url)
    page_data=loader.load().pop().page_content

    print(page_data)
    llm=llm_trans()
    res_json=llm.content_extarct(page_data)



    job_des=res_json
    print(job_des)
    skills=job_des['skills']
    
    links=pf.query_links(skills)

    mail_content=llm.email_content(job_des,links)

    st.write(mail_content)

    st.code(mail_content, language='markdown')