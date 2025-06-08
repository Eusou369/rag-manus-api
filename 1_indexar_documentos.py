import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter

print("Iniciando o processo de indexação...")

# --- Configuração do Modelo de Embedding Local ---
# Usando um modelo open-source poderoso que roda localmente. Custo zero.
# "BAAI/bge-m3" é um dos melhores modelos de embedding disponíveis.
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
print("Modelo de embedding carregado com sucesso.")

# --- Carregamento dos Documentos ---
# Lê todos os arquivos da pasta 'documentos'.
reader = SimpleDirectoryReader("./documentos")
documents = reader.load_data()
print(f"Carregados {len(documents)} documentos.")

# --- Configuração do Banco de Dados Vetorial Local (ChromaDB) ---
# O ChromaDB salva a base de dados em uma pasta local, sem custo.
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("manus_rag_demo")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# --- Divisão dos Documentos (Chunking) ---
# Divide os textos em pedaços menores e mais gerenciáveis.
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=20)

print("Iniciando a criação do índice vetorial. Isso pode levar alguns minutos...")

# --- Criação e Persistência do Índice ---
# Transforma os documentos em vetores e os armazena no ChromaDB.
# Este é o passo mais demorado, executado apenas uma vez.
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=embed_model,
    transformations=[splitter],
    show_progress=True,
)

print("=" * 50)
print("INDEXAÇÃO CONCLUÍDA COM SUCESSO!")
print(f"Sua base de conhecimento foi criada na pasta 'chroma_db'.")
print("Agora você pode executar o script '2_iniciar_api_perguntas.py'.")
print("=" * 50)

