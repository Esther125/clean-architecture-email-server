FROM python:3.10-slim AS build-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.10-slim AS development
ENV FASTAPI_ENV=development
WORKDIR /app/src
COPY --from=build-stage /tmp/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./src .
EXPOSE 8080
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8080", "--reload"]


FROM python:3.10-slim as production
ENV FASTAPI_ENV=production
WORKDIR /app/src
COPY --from=build-stage /tmp/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./src .
CMD ["fastapi", "run", "main.py", "--port", "8080"]