import os
import time
import torch
import pinecone

from io import BytesIO
from tqdm.auto import tqdm
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from PyPDF2 import PdfFileReader
from fastapi import FastAPI,UploadFile, File,HTTPException
from splade.models.transformer_rep import Splade
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI, File, Form, UploadFile, Response
from utils import extract_named_entities,chunker,builder,encode,search_pinecone
from transformers import AutoTokenizer, AutoModelForTokenClassification,pipeline

load_dotenv()
# set device to GPU if available
device = torch.cuda.current_device() if torch.cuda.is_available() else None
model_id_ner = os.getenv('model_id_ner')
dense_model_id=os.getenv("dense_model_id")
sparse_model_id = os.getenv("sparse_model_id")
api_key=os.getenv("api_key")  # app.pinecone.io
environment= os.getenv('environment')  # next to api key in console
index_name = os.getenv("index_name")
batch_size = int(os.getenv('batch_size'))


tokenizer_ner = AutoTokenizer.from_pretrained(
    model_id_ner
)
model_ner = AutoModelForTokenClassification.from_pretrained(
    model_id_ner
)
dense_model = SentenceTransformer(
    dense_model_id,
    device=device
)

sparse_model = Splade(sparse_model_id, agg='max')
sparse_model.to(device)  # move to GPU if possible
sparse_model.eval()
tokenizer_sparse = AutoTokenizer.from_pretrained(sparse_model_id)

nlp = pipeline(
    "ner",
    model=model_ner,
    tokenizer=tokenizer_ner,
    aggregation_strategy="max",
    device=device
)

pinecone.init(
    api_key=api_key,  # app.pinecone.io
    environment=environment  # next to api key in console
)
index = pinecone.GRPCIndex(index_name)

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreateDatabase(BaseModel):
    data: str
    
@app.post("/createDatabase")
async def create_item(file: UploadFile = File(...)):
    contents = await file.read()
    
    # # data=data.dict()
    # # data=data['data']
    
    # print(type(data))
    data=''
    if file.content_type == 'text/plain':
        data = contents.decode('utf-8')
    
        

    elif file.content_type == 'application/pdf':
        try:
            pdf = PdfFileReader(BytesIO(contents))

            text = ""
            for page_num in range(pdf.getNumPages()):
                page = pdf.getPage(page_num)
                text += page.extractText()

            data=text
        except Exception as e:
            raise HTTPException(status_code=400, detail="Unable to read PDF file")

    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    data1 = []
    chunks = chunker(data)
    print(chunks)
    for i, context in enumerate(chunks):
        data1.append({
            'id': f"{i}",
            'context': context,
            'NER':extract_named_entities(context,nlp)
        })
        
    
    
     
    try:
        pinecone.delete_index(index_name)
        print('11')
    except:
        print('not found')
        pass
    
    
    pinecone.create_index(
    index_name,
    dimension=768,
    metric="dotproduct",
    pod_type="s1"
    )
    
    time.sleep(10)
    
    
    
    print(index.describe_index_stats())
    
    for i in tqdm(range(0, len(data1), batch_size)):
        # extract batch of data
        i_end = min(i+batch_size, len(data1))
        batch = data1[i:i_end]
        
        
        # pass data to builder and upsert
        index.upsert(builder(data1[i:i+batch_size],dense_model,tokenizer_sparse,sparse_model,device))
        
    
    
    return 1
    
    
class Query(BaseModel):
    query: str
    
@app.post("/query")
async def create_item(query: Query):
    query=query.dict()
    query=query['query']
    search = [ i["metadata"] for i in search_pinecone(query,nlp,dense_model,tokenizer_sparse,sparse_model,device,index)[1]['matches']]
    return search
    

