# Use a imagem base oficial do Python
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do Flask
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o diretório de trabalho
COPY . .

# Expõe a porta que o Flask está escutando
EXPOSE 5000

# Define o comando para iniciar o servidor Flask
CMD ["python", "app.py"]
