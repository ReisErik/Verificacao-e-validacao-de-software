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

def validate_password(password: str):
    if not any(char.isdecimal() for char in password):
        raise HTTPException(
            status_code=400,
            detail="Senha deve conter pelo menos um caractere numerico."
        )
    if not any(char.isalpha() for char in password):
        raise HTTPException(
            status_code=400,
            detail="Senha deve conter pelo menos um caractere alfabetico."
        )
    if not any(not char.isalnum() for char in password):
        raise HTTPException(
            status_code=400,
            detail="Senha deve conter pelo menos um caractere especial."
        )

    return True