import os

class Config:
    # SECRET_KEY = 'SUPER SECRET'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SECRET_KEY = os.urandom(16)