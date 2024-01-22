FROM python:3.12-alpine

# Create pwd to container
WORKDIR /messenger

# Copiando pyproject.toml to /messenger
COPY pyproject.toml . 
# Copiando poetry.lock to /messenger
COPY poetry.lock .

RUN pip install poetry
# Desabilitando o uso de venv
RUN poetry config virtualenvs.create false
# installando as dependencias necessárias
RUN poetry install

# Copiando os arquivos do pwd para /messenger
COPY . .

ENTRYPOINT [ "python3", "main.py" ]
