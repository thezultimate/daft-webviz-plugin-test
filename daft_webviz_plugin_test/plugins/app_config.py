# Azure tenant ID (Equinor)
# This can be set as secret in Radix (mounted as env variable in the container)
TENANT_ID = "xx"

# Azure AD app client ID
# This is best to be set as secret in Radix (mounted as env variable in the container)
CLIENT_ID = "xx"

# Azure AD app client secret
# This is best to be set as secret in Radix (mounted as env variable in the container)
CLIENT_SECRET = "xx"

# Azure AD app scope
SCOPE = "xx"

# Auth server URL
AUTHORITY = "https://login.microsoftonline.com/" + TENANT_ID

# Secret key for Flask session
# This is best to be set as secret in Radix (mounted as env variable in the container)
SESSION_SECRET_KEY = "xx"

# Sumo base URL
SUMO_BASE_URL = "xx"
