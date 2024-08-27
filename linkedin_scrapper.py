from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv
import os
from mangum import Mangum

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PROXYCURL_API_KEY = os.getenv("PROXYCURL_API_KEY")
SCRAPIN_API_KEY = os.getenv("SCRAPIN_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class ProfileRequest(BaseModel):
    profile_url: str
    resume_id: int
    source_id: int


def scrape_profile_certifications(profile_url: str, resume_id: int, source_id: int):
    headers = {'Authorization': 'Bearer ' + PROXYCURL_API_KEY}
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    params = {
        'linkedin_profile_url': profile_url,
    }
    try:
        response = requests.get(api_endpoint, params=params, headers=headers)
        response.raise_for_status()
        profile_data = response.json()

        if 'certifications' in profile_data:
            for cert in profile_data['certifications']:
                year = cert.get('starts_at', {}).get('year')

                certification = {
                    'resume_id': resume_id,
                    'name': cert.get('name', ''),
                    'issued_by': cert.get('authority', ''),
                    'year': year,
                    'issuing_organization': cert.get('authority', ''),
                    'is_verified': True,
                    'source_id': source_id,
                    'license_number': cert.get('license_number'),
                    'url': cert.get('url')
                }

                supabase.table('resume_certifications').insert(certification).execute()

        return len(profile_data.get('certifications', []))
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while scraping certifications: {str(e)}"
        )


def scrape_profile_recommendations(profile_url: str, resume_id: int):
    url = "https://api.scrapin.io/enrichment/profile"
    querystring = {
        "SCRAPIN_API_KEY": SCRAPIN_API_KEY,
        "linkedInUrl": profile_url
    }

    try:
        response = requests.request("GET", url, params=querystring)
        response.raise_for_status()
        profile_data = response.json()

        recommendations_count = 0
        if 'recommendations' in profile_data:
            for rec in profile_data['recommendations']:
                date_str = rec.get('caption', '').split(',')[0]
                try:
                    date = datetime.strptime(date_str, "%B %d, %Y").date()
                except ValueError:
                    date = None

                recommender_name = rec.get('authorFullname', '')
                recommender_parts = recommender_name.split()
                recommender_first_name = recommender_parts[0] if recommender_parts else ''
                recommender_last_name = ' '.join(recommender_parts[1:]) if len(recommender_parts) > 1 else ''

                recommendation = {
                    'resume_id': resume_id,
                    'content': rec.get('description', ''),
                    'recommender_name': recommender_name,
                    'recommender_first_name': recommender_first_name,
                    'recommender_last_name': recommender_last_name,
                    'recommender_title': '',
                    'recommender_company': '',
                    'recommender_url': rec.get('authorUrl', ''),
                    'source': 'LinkedIn',
                    'date': date
                }

                supabase.table('recommendations').insert(recommendation).execute()
                recommendations_count += 1

        return recommendations_count
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while scraping recommendations: {str(e)}"
        )


@app.post("/scrape-linkedin-profile")
async def scrape_linkedin_profile(profile_request: ProfileRequest):
    try:
        certifications_count = scrape_profile_certifications(
            profile_request.profile_url,
            profile_request.resume_id,
            profile_request.source_id
        )
        recommendations_count = scrape_profile_recommendations(
            profile_request.profile_url,
            profile_request.resume_id
        )

        return {
            "message": "Profile scraped successfully",
            "certifications_added": certifications_count,
            "recommendations_added": recommendations_count
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
def handler(event, context):
    return mangum_handler(app, event, context)

mangum_handler = Mangum(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)