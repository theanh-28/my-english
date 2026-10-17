FROM python:3.13-slim
WORKDIR /app
COPY server.py manage.py sample.json add_topics.py grammar_catalog.py ./
COPY web ./web
ENV HOST=0.0.0.0 PORT=8765 DATABASE_PATH=/data/learning.sqlite3
VOLUME ["/data"]
EXPOSE 8765
CMD ["python", "server.py"]
