from fastapi import HTTPException

def validate_unique_name(unique_name: str):
    if not unique_name:
        raise HTTPException(
            status_code=400,
            detail="Unique name é obrigatório."
        )
    if not unique_name.isalnum():
        raise HTTPException(
            status_code=400,
            detail="Unique name deve conter apenas caracteres alfanuméricos."
        )

    return True