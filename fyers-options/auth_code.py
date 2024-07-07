client_id = ""
redirect_uri = ""
auth_url = f"https://api.fyers.in/api/v2/generate-authcode?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state=sample_state"
print(f"Go to the following URL to authorize your application: \n{auth_url}")
