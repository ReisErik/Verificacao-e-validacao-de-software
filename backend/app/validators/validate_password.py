from fastapi import HTTPException

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