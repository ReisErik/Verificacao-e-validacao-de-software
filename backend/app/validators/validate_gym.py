from fastapi import HTTPException

def validate_gym(name: str, location: str, owner_id: int):
    if not name or not location:
        raise HTTPException(status_code=400, detail="Nome e localizacao sao obrigatorios.")
    
    if owner_id is None:
        raise HTTPException(status_code=400, detail="Owner id é obrigatório.")
    
    if not all (char.isalnum() or char.isspace() for char in name):
        raise HTTPException(status_code=400, detail="Nome deve conter apenas caracteres alfanumericos.")

    if not all (char.isalnum() or char.isspace() for char in location):
        raise HTTPException(status_code=400, detail="Localizacao deve conter apenas caracteres alfanumericos.")
    
    return True