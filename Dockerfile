# Usa uma imagem base leve com Python 3.10
FROM python:3.10-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia todos os arquivos do seu projeto para dentro do contêiner
COPY . .

# Instala as bibliotecas Python listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# O comando que será executado para iniciar a API
CMD ["uvicorn", "2_iniciar_api_perguntas:app", "--host", "0.0.0.0", "--port", "7860"]