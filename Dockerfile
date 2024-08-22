FROM python:3.10-slim AS build-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN cat requirements.txt


FROM python:3.10-slim AS development
WORKDIR /src
COPY --from=build-stage /tmp/requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
COPY ./src /src
EXPOSE 8080
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8080"]

