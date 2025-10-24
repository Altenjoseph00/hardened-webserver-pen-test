FROM python:3.11-slim
WORKDIR /app
COPY web/ /app/web/
EXPOSE 80
CMD ["python3", "-m", "http.server", "80"]
