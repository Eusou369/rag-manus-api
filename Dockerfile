# Usa uma imagem Python oficial como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências para o contêiner
COPY requirements.txt requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copia TODOS os arquivos do projeto para o contêiner
COPY . .

# Dá permissão de execução para o script de inicialização
RUN chmod +x startup.sh

# Comando padrão para iniciar a aplicação via script
CMD ["./startup.sh"]