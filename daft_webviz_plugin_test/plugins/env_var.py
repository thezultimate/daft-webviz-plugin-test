import os
from ..plugins import app_config as App_config

def get_tenant_id():
    return os.getenv(key="TENANT_ID", default=App_config.TENANT_ID)

def get_client_id():
    return os.getenv(key="CLIENT_ID", default=App_config.CLIENT_ID)

def get_client_secret():
    return os.getenv(key="CLIENT_SECRET", default=App_config.CLIENT_SECRET)

def get_scope():
    return os.getenv(key="SCOPE", default=App_config.SCOPE)

def get_authority():
    return os.getenv(key="AUTHORITY", default=App_config.AUTHORITY)

def get_session_secret_key():
    return os.getenv(key="SESSION_SECRET_KEY", default=App_config.SESSION_SECRET_KEY)

def get_sumo_base_url():
    return os.getenv(key="SUMO_BASE_URL", default=App_config.SUMO_BASE_URL)