import torch

def extract_named_entities(text,nlp):
    # extract named entities using the NER pipeline
    extracted = nlp(text)
    ner=''
    # loop through the results and only select the entity names
    
    ner = list(set([entity["word"] for entity in extracted]))
        
    return ner

def chunker(contexts: list):
    limit = 384
    chunks = []
    all_contexts = ''.join(contexts).split('.')
    chunk = []
    
    for context in all_contexts:
        chunk.append(context)
        if len(chunk) >= 3 and len('.'.join(chunk)) > limit:
            # surpassed limit so add to chunks and reset
            chunks.append('.'.join(chunk).strip()+'.')
            # add some overlap between passages
            chunk = chunk[-1:]
    # if we finish and still have a chunk, add it
    if chunk is not None:
        chunks.append('.'.join(chunk))
        
    return chunks



def builder(records: list,dense_model,tokenizer_sparse,sparse_model,device):
    ids = [x['id'] for x in records]
    contexts = [x['context'] for x in records]
    Ners=[x['NER'] for x in records]
    # create dense vecs
    dense_vecs = dense_model.encode(contexts).tolist()
    # create sparse vecs
    input_ids = tokenizer_sparse(
        contexts, return_tensors='pt',
        padding=True, truncation=True
    )
    with torch.no_grad():
        sparse_vecs = sparse_model(
            d_kwargs=input_ids.to(device)
        )['d_rep'].squeeze()
    # convert to upsert format
    upserts = []
    for _id, dense_vec, sparse_vec, context,Ner in zip(ids, dense_vecs, sparse_vecs, contexts,Ners):
        # extract columns where there are non-zero weights
        indices = sparse_vec.nonzero().squeeze().cpu().tolist()  # positions
        values = sparse_vec[indices].cpu().tolist()  # weights/scores
        # build sparse values dictionary
        sparse_values = {
            "indices": indices,
            "values": values
        }
        # build metadata struct
        metadata = {'context': context,'Ner':Ner}
        # append all to upserts list as pinecone.Vector (or GRPCVector)
        upserts.append({
            'id': _id,
            'values': dense_vec,
            'sparse_values': sparse_values,
            'metadata': metadata
        })
    return upserts



def encode(text: str ,dense_model,tokenizer_sparse,sparse_model,device):
    # create dense vec
    dense_vec = dense_model.encode(text).tolist()
    # create sparse vec
    input_ids = tokenizer_sparse(text, return_tensors='pt')
    with torch.no_grad():
        sparse_vec = sparse_model(
            d_kwargs=input_ids.to(device)
        )['d_rep'].squeeze()
    # convert to dictionary format
    indices = sparse_vec.nonzero().squeeze().cpu().tolist()
    values = sparse_vec[indices].cpu().tolist()
    sparse_dict = {"indices": indices, "values": values}
    # return vecs
    return dense_vec, sparse_dict

def search_pinecone(query,nlp,dense_model,tokenizer_sparse,sparse_model,device,index):
    # extract named entities from the query
    ne = extract_named_entities(query,nlp)[0]
    dense, sparse = encode(query,dense_model,tokenizer_sparse,sparse_model,device)
    # create embeddings for the query
    xc = index.query(
    vector=dense,
    sparse_vector=sparse,
    top_k=10,  
    include_metadata=True,
)
    
    # query the pinecone index while applying named entity filter
    
    return ne, xc