# Import the required module from the fyers_apiv3 package
from fyers_apiv3 import fyersModel

from config import need

# Define your Fyers API credentials
client_id = need("FYERS_CLIENT_ID")
secret_key = need("FYERS_SECRET_KEY")
redirect_uri = need("FYERS_REDIRECT_URI")
response_type = "code" 
grant_type = "authorization_code"  

# The authorization code received from Fyers after the user grants access
auth_code = need("FYERS_AUTH_CODE")

# Create a session object to handle the Fyers API authentication and token generation
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key, 
    redirect_uri=redirect_uri, 
    response_type=response_type, 
    grant_type=grant_type
)

# Set the authorization code in the session object
session.set_token(auth_code)

# Generate the access token using the authorization code
response = session.generate_token()

# Print the response, which should contain the access token and other details
print(response)
