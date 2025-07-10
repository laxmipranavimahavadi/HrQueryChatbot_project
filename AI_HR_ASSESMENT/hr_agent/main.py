import os, json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Ollama

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

EMPLOYEE_FILE = "employees.json"
embed_func = SpacyEmbeddings(model_name="en_core_web_md")

class Query(BaseModel):
    question: str

class NewEmployee(BaseModel):
    name: str
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: str

def load_employees():
    if not os.path.exists(EMPLOYEE_FILE):
        raise FileNotFoundError("Please create employees.json")
    with open(EMPLOYEE_FILE, "r") as f:
        data = json.load(f)

    documents = []
    for emp in data.get("employees", []):
        content = (
            f"Name: {emp['name']}\n"
            f"Skills: {', '.join(emp['skills'])}\n"
            f"Experience: {emp['experience_years']} years\n"
            f"Projects: {', '.join(emp['projects'])}\n"
            f"Availability: {emp['availability']}"
        )
        documents.append(Document(page_content=content, metadata={"name": emp["name"]}))
    return documents

def add_employee(new_emp: dict):
    with open(EMPLOYEE_FILE, "r") as f:
        data = json.load(f)
    data["employees"].append(new_emp)
    with open(EMPLOYEE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def split_docs(docs):
    return RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20).split_documents(docs)

def get_retriever(docs):
    if not os.path.exists("db"):
        db = Chroma.from_documents(split_docs(docs), embed_func, persist_directory="db", collection_name="employees")
        db.persist()
    else:
        db = Chroma(embedding_function=embed_func, persist_directory="db", collection_name="employees")
    return db.as_retriever()

def get_chain():
    docs = load_employees()
    retriever = get_retriever(docs)
    llm = Ollama(model="tinyllama")
    return ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)

chain = get_chain()

@app.post("/chat")
async def chat(req: Query):
    return {"response": chain.invoke({"question": req.question, "chat_history": []})}


@app.post("/employees/add")
async def add_emp(req: NewEmployee):
    add_employee(req.dict())
    global chain
    chain = get_chain()  # reload updated chain
    return JSONResponse(content={"message": f"{req.name} added successfully."})
