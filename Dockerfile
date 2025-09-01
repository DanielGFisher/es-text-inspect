FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m nltk.downloader vader_lexicon

EXPOSE 8000

CMD ["uvicorn", "src:main:app", "--host", "0.0.0.0", "--port", "8000"]