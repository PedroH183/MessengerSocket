FROM python:3.12-alpine

WORKDIR /messenger

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

ENTRYPOINT [ "python3", "main.py" ]
