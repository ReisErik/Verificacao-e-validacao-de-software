from fastapi import HTTPException

def validateAuth(current_user):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")