from config import need

client_id = need("FYERS_CLIENT_ID")
redirect_uri = need("FYERS_REDIRECT_URI")
auth_url = f"https://api.fyers.in/api/v2/generate-authcode?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state=sample_state"
print(f"Go to the following URL to authorize your application: \n{auth_url}")
