import uvicorn
import chromadb
from fastapi import FastAPI
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

# --- Modelo para a requisição da API ---
class QueryRequest(BaseModel):
    question: str

# --- Inicialização da Aplicação FastAPI ---
app = FastAPI(
    title="API do Sistema RAG para Manus",
    description="Faça uma pergunta sobre os documentos e receba uma resposta gerada por IA.",
    version="1.0.0",
)

# --- Carregamento dos Componentes do RAG ---
# Esta seção é executada apenas uma vez quando a API inicia.
def load_rag_pipeline():
    print("Carregando pipeline RAG...")
    # Conecta ao banco de dados vetorial local já existente
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("manus_rag_demo")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # Carrega o mesmo modelo de embedding usado na indexação
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

    # Carrega o índice a partir do banco vetorial
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
    )

    # Configura o LLM local via Ollama
    # 'host.docker.internal' permite que o contêiner Docker fale com o Ollama na máquina hospedeira
    llm = Ollama(model="llama3", request_timeout=120.0, base_url="http://host.docker.internal:11434")

    # Configura o retriever (buscador)
    retriever = VectorIndexRetriever(index=index, similarity_top_k=4)

    # Configura o sintetizador de respostas
    response_synthesizer = get_response_synthesizer(response_mode="compact", llm=llm)

    # Monta o "motor" de perguntas e respostas
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )
    print("Pipeline RAG carregado com sucesso!")
    return query_engine

# Carrega o motor RAG e o armazena em uma variável global
query_engine_global = load_rag_pipeline()

@app.post("/query")
def process_query(req: QueryRequest):
    """
    Recebe uma pergunta, busca a informação nos documentos e gera uma resposta.
    """
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

# --- Ponto de Entrada para Execução do Servidor ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

