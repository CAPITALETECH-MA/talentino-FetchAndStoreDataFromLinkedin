FROM python:3.9-slim

WORKDIR /SCRAPPER

COPY . /SCRAPPER/

RUN pip install --no-cache-dir fastapi uvicorn requests supabase python-dotenv

EXPOSE 8000

ENV SUPABASE_URL=""
ENV SUPABASE_KEY=""
ENV PROXYCURL_API_KEY=""
ENV SCRAPIN_API_KEY=""

CMD ["uvicorn", "app:linkedin_scrapper", "--host", "0.0.0.0", "--port", "8000"]