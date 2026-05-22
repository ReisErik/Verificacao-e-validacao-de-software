from fastapi import HTTPException

def validate_name(first_name: str, last_name: str):
    if not first_name or not last_name:
        raise HTTPException(
            status_code=400,
            detail="Nome e sobrenome são obrigatórios."
        )
    if not first_name.replace(" ", "").isalpha() or not last_name.replace(" ", "").isalpha():
        raise HTTPException(
            status_code=400,
            detail="Nome e sobrenome devem conter apenas caracteres alfabéticos."
        )

    return True