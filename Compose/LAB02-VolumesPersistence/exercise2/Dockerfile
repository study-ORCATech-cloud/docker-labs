FROM python:3.9-slim

WORKDIR /app

COPY ./app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# No need to COPY application code since we'll use bind mounts
# for development to reflect changes immediately

EXPOSE 8080

CMD ["python", "app.py"] 