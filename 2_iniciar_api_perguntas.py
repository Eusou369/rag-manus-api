import uvicorn
import chromadb
import os 
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv 
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceInferenceAPI 
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

# Carrega as variáveis do arquivo .env (o token HF_TOKEN)
load_dotenv() 

class QueryRequest(BaseModel):
    question: str

app = FastAPI(
    title="API do Sistema RAG para Manus (Hugging Face)",
    description="Faça uma pergunta sobre os documentos e receba uma resposta gerada por IA na nuvem.",
    version="1.1.0",
)

def load_rag_pipeline():
    print("Carregando pipeline RAG...")
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("manus_rag_demo")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
    )

    # --- MUDANÇA PRINCIPAL: De Ollama para Hugging Face ---
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("Token do Hugging Face não encontrado! Verifique seu arquivo .env")

    llm = HuggingFaceInferenceAPI(
        model_name="mistralai/Mixtral-8x7B-Instruct-v0.1",
        token=hf_token
    )
    # --- FIM DA MUDANÇA ---

    retriever = VectorIndexRetriever(index=index, similarity_top_k=4)

    response_synthesizer = get_response_synthesizer(response_mode="compact", llm=llm)

    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )
    print("Pipeline RAG carregado com sucesso!")
    return query_engine

query_engine_global = load_rag_pipeline()

@app.post("/query")
def process_query(req: QueryRequest):
    print(f"Recebida a pergunta: {req.question}")
    response = query_engine_global.query(req.question)

    return {
        "question": req.question,
        "answer": response.response,
        "source_nodes": [
            {
                "file_name": node.metadata.get('file_name', 'N/A'),
                "score": node.score
            }
            for node in response.source_nodes
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)