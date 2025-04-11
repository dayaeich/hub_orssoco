# Usa imagem oficial do Python
FROM python:3.11-slim

# Evita perguntas interativas e define variáveis para produção
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas os arquivos necessários primeiro (melhor para cache do Docker)
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia o restante do código-fonte
COPY . .

# Expõe a porta que o Flask vai usar (Cloud Run usa 8080)
EXPOSE 8080

# Define o comando padrão para rodar o servidor Flask
CMD ["python", "server.py"]
