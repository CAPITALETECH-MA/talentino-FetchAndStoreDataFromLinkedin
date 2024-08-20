FROM python:3.9-slim

WORKDIR /SCRAPPER

COPY . /SCRAPPER/

RUN pip install --no-cache-dir fastapi uvicorn requests supabase python-dotenv

EXPOSE 8000

ENV SUPABASE_URL="https://abjtqzgnrtsikkqgnqeg.supabase.co"
ENV SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFianRxemducnRzaWtrcWducWVnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDYwMjQ0MTIsImV4cCI6MjAyMTYwMDQxMn0.53U1JW8NNM_8ZmVISwnSXQ1LtWSNZQv_Gy5AM33SZaY"
ENV PROXYCURL_API_KEY="CWj8gOnyW9BtdgWy6QQt_g"
ENV SCRAPIN_API_KEY="your_scrapin_api_key"
ENV API_KEY="sk_live_66c098c0eb3ad40659786024_key_wa7r7sa0o6"

CMD ["uvicorn", "app:linkedin_scrapper", "--host", "0.0.0.0", "--port", "8000"]