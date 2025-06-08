# Kit de Demonstração - Sistema RAG para Manus

Este projeto demonstra um sistema de Retrieval-Augmented Generation (RAG) completo, configurado para rodar localmente com custo zero de API, facilitando a avaliação e integração com a plataforma Manus.

## Pré-requisitos

1.  **Docker:** A maneira mais fácil de executar. Instale o [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2.  **Ollama:** Para rodar o modelo de linguagem localmente. Instale o [Ollama](https://ollama.com/) e, após a instalação, execute no terminal:
    ```bash
    ollama pull llama3
    ```

## Como Executar (Método Recomendado com Docker)

1.  **Coloque os Documentos:** Adicione os arquivos PDF, DOCX e TXT que deseja analisar dentro da pasta `documentos/`.
2.  **Construa a Imagem Docker:** No terminal, na pasta raiz do projeto, execute:
    ```bash
    docker build -t rag-manus-demo .
    ```
3.  **Execute os Contêineres:**
    * **Passo 1: Indexar Documentos (Execute apenas uma vez)**
        ```bash
        docker run --rm -v ./documentos:/app/documentos -v ./chroma_db:/app/chroma_db rag-manus-demo python 1_indexar_documentos.py
        ```
        *Isso irá "ler" os documentos e criar uma base de conhecimento na nova pasta `chroma_db`.*

    * **Passo 2: Iniciar a API para Perguntas**
        ```bash
        docker run --rm -p 8000:8000 -v ./chroma_db:/app/chroma_db --add-host=host.docker.internal:host-gateway rag-manus-demo
        ```
        *Isso inicia o servidor. A flag `--add-host` é crucial para permitir que o contêiner se comunique com o Ollama rodando na sua máquina.*

4.  **Teste a API:** Abra seu navegador e acesse [http://localhost:8000/docs](http://localhost:8000/docs). Você verá uma interface interativa para fazer perguntas.

## Como Testar via Terminal (Exemplo)

```bash
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"question": "Qual o procedimento de segurança para a máquina A?"}'
```

