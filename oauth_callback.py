from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
REDIRECT_URI = "https://magnoliaaiexperts.com/api/oauth_callback"

@app.get("/api/oauth_callback")
async def oauth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No authorization code provided"}

    token_url = "https://accounts.zoho.com/oauth/v2/token"
    params = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }

    response = requests.post(token_url, params=params)

    if response.status_code == 200:
        tokens = response.json()
        # For demo: return the tokens (in production, save securely)
        return {
            "message": "Zoho OAuth successful!",
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
            "expires_in": tokens.get("expires_in")
        }
    else:
        return {"error": "Token exchange failed", "details": response.text}
