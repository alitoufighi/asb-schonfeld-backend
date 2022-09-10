FROM dineshsonachalam/tech-courses-search-engine-backend:latest

WORKDIR /app

# COPY requirements.txt .

# RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000

# RUN chmod +x /app/main.py

CMD ["python3", "main.py"]
