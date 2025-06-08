#!/bin/bash

# Define o caminho do banco de dados
DB_PATH="./chroma_db"

# Verifica se a pasta do banco de dados NÃO existe
if [ ! -d "$DB_PATH" ]; then
    echo "Pasta chroma_db não encontrada. Executando a indexação pela primeira vez..."
    python 1_indexar_documentos.py
else
    echo "Pasta chroma_db já existe. Pulando a indexação."
fi

# Inicia a API
echo "Iniciando a API de perguntas..."
uvicorn 2_iniciar_api_perguntas:app --host 0.0.0.0 --port 7860