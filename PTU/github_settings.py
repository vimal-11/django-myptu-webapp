# Copy this file to github_settings.py (don't check it into github)  #jhyf

# Go to https://github.com/settings/developers

# Add a New OAuth2 App 

# Using PythonAnywhere here are some settings:

# Application name: ChuckList PythonAnywhere
# Homepage Url: https://drchuck.pythonanywhere.com
# Application Description: Whatever
# Authorization callback URL: https://drchuck.pythonanywhere.com/oauth/complete/github/

# Also on PythonAnywhere, go into the Web tab and enable "Force HTTPS"
# so you don't get a redirect URI mismatch.

# Then copy the client_key and secret to this file

SOCIAL_AUTH_GITHUB_KEY = 'c2b06332c32e3cbc2ac0'
SOCIAL_AUTH_GITHUB_SECRET = 'a25fb0280d22cb8fd87d23115f46062f47a6a6ae'

# Ask for the user's email (don't edit this line)
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

# Note you may not get email for github users that don't make their
# email public - that is OK

# For detail: https://readthedocs.org/projects/python-social-auth/downloads/pdf/latest/

# Using ngrok is hard because the url changes every time you start ngrok

# If you are running on localhost, here are some settings:

# Application name: ChuckList Local
# Homepage Url: http://localhost:8000
# Application Description: Whatever
# Authorization callback URL: http://127.0.0.1:8000/oauth/complete/github/