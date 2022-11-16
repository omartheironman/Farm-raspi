
import secrets
import os
from fastapi.security import HTTPBasic, HTTPBasicCredentials

def get_auth(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    correct_username = secrets.compare_digest(credentials.username, os.getEnv("Username"))
    correct_password = secrets.compare_digest(credentials.password, os.getEnv("Password"))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
