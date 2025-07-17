from fastapi import FastAPI
import requests
import os

app = FastAPI()

CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")  # Set this in Vercel

@app.get("/api/refresh_token")
async def refresh_zoho_token():
    url = "https://accounts.zoho.com/oauth/v2/token"
    params = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, params=params)

    if response.status_code == 200:
        tokens = response.json()
        return {
            "message": "Access token refreshed!",
            "access_token": tokens.get("access_token"),
            "expires_in": tokens.get("expires_in")
        }
    else:
        return {"error": "Token refresh failed", "details": response.text}
