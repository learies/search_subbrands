FROM python:3.13-alpine
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /code
COPY pyproject.toml .
RUN pip install --no-cache-dir uv && \
    uv venv && \
    uv pip install --no-cache-dir -e .
COPY . .
CMD ["uv", "run", "main.py"]