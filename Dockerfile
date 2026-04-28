FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY hermesforge_mcp/ hermesforge_mcp/

RUN pip install --no-cache-dir mcp>=1.0.0 requests>=2.28.0 hatchling && \
    pip install --no-cache-dir -e .

ENV HERMESFORGE_API_KEY=""
ENV MCP_TRANSPORT="sse"

EXPOSE 8000

CMD ["hermesforge-mcp"]
